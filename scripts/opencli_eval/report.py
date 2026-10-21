#!/usr/bin/env python
# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Build the M4 evaluation report from a run manifest and the stored sessions.

For every run it reads ``~/.jiuwenswarm/agent/sessions/<session_id>/history.jsonl``
and extracts: the final reply and its structural check, wall time, main-agent
tokens (``chat.usage_summary``), the Browser Agent's own model usage
(``browser_result.model_usage``), OpenCLI vs page tool calls, whether the first
action was a delegation to ``browser_agent``, ``needs_user`` blocks and
``unbacked_items``. Writes ``report.md`` and ``runs.csv`` next to the manifest.

Example::

    uv run python scripts/opencli_eval/report.py scripts/opencli_eval/runs/<timestamp>/manifest.jsonl
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
SESSIONS = Path.home() / ".jiuwenswarm" / "agent" / "sessions"
# The Browser runtime's own step log (on by default; written in the backend's working directory).
BROWSER_LOG = HERE.parents[1] / "logs" / "browser_agent.log"
LINK_RE = re.compile(r"https?://[^\s<>\"'`()\[\]，。；、|]+")


def _browser_results(text: str) -> list[dict[str, Any]]:
    """browser_result payloads inside a stored tool result (a Python repr around JSON)."""
    found = []
    start = text.find("{'output'")
    if start >= 0:
        try:
            output = ast.literal_eval(text[start:text.rfind("}") + 1]).get("output", "")
            text = output if isinstance(output, str) else text
        except (ValueError, SyntaxError):
            pass
    index = text.find('{"browser_result"')
    while index >= 0:
        try:
            payload, end = json.JSONDecoder(strict=False).raw_decode(text[index:])
            found.append(payload["browser_result"])
            index = text.find('{"browser_result"', index + end)
        except (ValueError, KeyError):
            break
    return found


def load_browser_steps(log_path: Path) -> dict[str, list[dict[str, Any]]]:
    """Ordered Browser Agent steps per sub-session, from the existing [BROWSER_SUBAGENT] status events."""
    steps: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if not log_path.is_file():
        return steps
    with log_path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            marker = line.find("[BROWSER_SUBAGENT] {")
            if marker < 0:
                continue
            try:
                event = json.loads(line[marker + len("[BROWSER_SUBAGENT] "):])
            except ValueError:
                continue
            if event.get("phase") in ("tool_start", "model_end", "task_end"):
                steps[str(event.get("session_id") or "")].append(event)
    return steps


def tool_sequence(steps: dict[str, list[dict[str, Any]]], session_id: str) -> list[str]:
    """Tool names in call order across this chat's Browser Agent sub-sessions."""
    prefix = f"{session_id}_sub_browser_agent_"
    return [event["tool_name"] for sub, events in steps.items() if sub.startswith(prefix)
            for event in events if event.get("phase") == "tool_start" and event.get("tool_name")]


def _kind(tool: str) -> str:
    return "opencli" if tool == "opencli_run" else ("describe" if tool == "opencli_describe" else "page")


def follows(sequence: list[str], pattern: list[str]) -> bool:
    """Whether the tool kinds contain ``pattern`` in order, e.g. ["opencli", "page", "opencli"]."""
    kinds, index = [_kind(tool) for tool in sequence], 0
    for kind in kinds:
        if index < len(pattern) and kind == pattern[index]:
            index += 1
    return index == len(pattern)


STEPS: dict[str, list[dict[str, Any]]] = {}


def analyse(record: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> dict[str, Any]:
    row: dict[str, Any] = {key: record.get(key) for key in ("task", "group", "arm", "run", "session_id", "wall_s")}
    row.update(timed_out=bool(record.get("timed_out")), asked_user=record.get("asked_user"),
               driver_error=record.get("error"))
    history = SESSIONS / str(record.get("session_id")) / "history.jsonl"
    events = [json.loads(line) for line in history.read_text(encoding="utf-8").splitlines() if line.strip()] \
        if history.is_file() else []
    finals = [e.get("content") or "" for e in events if e.get("event_type") == "chat.final" and e.get("content")]
    calls = [e["tool_call"]["name"] for e in events if e.get("event_type") == "chat.tool_call"]
    first_args = next((e["tool_call"].get("arguments") or "" for e in events if e.get("event_type") == "chat.tool_call"), "")
    usage = next((e.get("usage") or {} for e in reversed(events) if e.get("event_type") == "chat.usage_summary"), {})
    results = [r for e in events if e.get("event_type") == "chat.tool_result"
               for r in _browser_results(str(e.get("result") or e.get("content") or ""))]
    reply = finals[-1] if finals else ""
    check = tasks.get(row["task"], {}).get("check", {})
    links = [link for link in LINK_RE.findall(reply) if check.get("link_domain", "") in link]
    browser_usage: dict[str, float] = defaultdict(float)
    by_name: dict[str, int] = defaultdict(int)
    for result in results:
        model = result.get("model_usage") or {}
        for key in ("model_calls", "tool_calls", "input_tokens", "output_tokens", "cache_tokens", "total_cost"):
            browser_usage[key] += float(model.get(key) or 0)
        for name, count in (model.get("tool_calls_by_name") or {}).items():
            by_name[name] += int(count)
    opencli_calls = sum(count for name, count in by_name.items() if name.startswith("opencli_"))
    opencli_runs = int(by_name.get("opencli_run", 0))
    page_tools = sum(count for name, count in by_name.items() if not name.startswith("opencli_"))
    # Flow checks for chain tasks: enough command runs and page steps (counts only; order is not recorded).
    flow_ok = opencli_runs >= int(check.get("min_opencli_runs") or 0) and page_tools >= int(check.get("min_page_tools") or 0)
    sequence = tool_sequence(STEPS, str(record.get("session_id")))
    if check.get("flow_order"):
        # Order needs the step log; without it the count check above is all we can say.
        flow_ok = flow_ok and (follows(sequence, list(check["flow_order"])) if sequence else False)
    statuses = [str(r.get("status")) for r in results]
    row.update(
        delegated=calls[:1] == ["task_tool"] and "browser_agent" in first_args,
        browser_tasks=len(results),
        browser_status="/".join(statuses),
        needs_user=any(str(r.get("terminal_reason") or "").startswith("external_user_action") or "needs_user" in
                       json.dumps(r.get("blockers") or [], ensure_ascii=False) for r in results),
        unbacked=sum(len(r.get("unbacked_items") or []) for r in results),
        links=len(set(links)),
        check_passed=bool(reply) and len(set(links)) >= int(check.get("min_links") or 0),
        opencli_runs=opencli_runs,
        flow_ok=flow_ok,
        tool_sequence=">".join(_kind(tool)[0] if _kind(tool) != "page" else tool.rsplit("_", 1)[-1] for tool in sequence),
        main_input_tokens=int(usage.get("input_tokens") or 0),
        main_output_tokens=int(usage.get("output_tokens") or 0),
        main_cost=float(usage.get("total_cost") or 0),
        browser_model_calls=int(browser_usage["model_calls"]),
        browser_tool_calls=int(browser_usage["tool_calls"]),
        opencli_calls=opencli_calls,
        page_tool_calls=int(browser_usage["tool_calls"]) - opencli_calls,
        browser_input_tokens=int(browser_usage["input_tokens"]),
        browser_output_tokens=int(browser_usage["output_tokens"]),
        browser_cost=round(browser_usage["total_cost"], 4),
    )
    row["total_tokens"] = (row["main_input_tokens"] + row["main_output_tokens"]
                           + row["browser_input_tokens"] + row["browser_output_tokens"])
    row["total_cost"] = round(row["main_cost"] + row["browser_cost"], 4)
    row["success"] = row["check_passed"] and row["flow_ok"] and not row["timed_out"] and not row["driver_error"]
    return row


def _median(values: list[float], digits: int = 1) -> float:
    return round(statistics.median(values), digits) if values else 0.0


def summarize(rows: list[dict[str, Any]], key: str) -> list[str]:
    lines = [f"| {key} | arm | runs | success | median wall s | median browser model calls | median total tokens |"
             " median cost | OpenCLI calls | delegated first | needs_user | unbacked |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(str(row[key]), str(row["arm"]))].append(row)
    for (name, arm), items in sorted(groups.items()):
        lines.append(
            f"| {name} | {arm} | {len(items)} | {sum(r['success'] for r in items)}/{len(items)} | "
            f"{_median([r['wall_s'] or 0 for r in items])} | {_median([r['browser_model_calls'] for r in items])} | "
            f"{_median([r['total_tokens'] for r in items]):.0f} | {_median([r['total_cost'] for r in items], 4):.3f} | "
            f"{sum(r['opencli_calls'] for r in items)} | {sum(r['delegated'] for r in items)}/{len(items)} | "
            f"{sum(r['needs_user'] for r in items)} | {sum(r['unbacked'] for r in items)} |"
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("manifest")
    parser.add_argument("--browser-log", default=str(BROWSER_LOG), help="the Browser runtime's step log")
    args = parser.parse_args()
    STEPS.update(load_browser_steps(Path(args.browser_log)))
    manifest = Path(args.manifest)
    tasks = {task["id"]: task for task in json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))["tasks"]}
    rows = [analyse(json.loads(line), tasks) for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()]
    with (manifest.parent / "runs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["task"])
        writer.writeheader()
        writer.writerows(rows)
    report = [
        "# OpenCLI M4 evaluation", "",
        f"Manifest: `{manifest}`. Runs: {len(rows)}. C2 (deferred MCP start) not enabled.", "",
        "Success = the final reply passes the task's structural check (enough links on the expected domain), "
        "without timeout or driver error. Total tokens = main agent + Browser Agent.", "",
        "## By arm", "", *summarize(rows, "arm"), "",
        "## By task group", "", *summarize(rows, "group"), "",
        "## By task", "", *summarize(rows, "task"), "",
    ]
    (manifest.parent / "report.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
