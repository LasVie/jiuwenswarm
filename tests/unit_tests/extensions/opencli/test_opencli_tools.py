# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""opencli_describe / opencli_run: classification, confirmation, pending writes, size cap."""

from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path

import pytest

from jiuwenswarm.extensions.opencli.catalog import Catalog, CommandCancelled, RunOutcome
from jiuwenswarm.extensions.opencli.pending import PendingStore
from jiuwenswarm.extensions.opencli.tools import (
    RESULT_LIMIT_BYTES,
    OpenCLIDescribeTool,
    OpenCLIRunTool,
    OpenCLIToolContext,
    fit_result,
)
from jiuwenswarm.extensions.opencli.worker_page import AwaitingUser

CATALOG = Catalog.from_payload(
    {
        "commands": [
            {"site": "demo", "command": "search", "access": "read", "needs_browser": True,
             "columns": ["title", "url"],
             "args": [{"name": "query", "type": "str", "required": True, "positional": True}]},
            {"site": "demo", "command": "follow", "access": "write", "needs_browser": True,
             "args": [{"name": "uid", "type": "str", "required": True}]},
            {"site": "api", "command": "top", "access": "read", "needs_browser": False, "args": []},
        ]
    },
    source="opencli",
)


class FakeSource:
    id = "opencli"

    def __init__(self) -> None:
        self.outcome = RunOutcome(started=True, category="ok", rows=[{"title": "t", "url": "u"}], exit_code=0)
        self.calls: list[tuple[str, str | None]] = []

    def catalog(self) -> Catalog:
        return CATALOG

    async def run(self, spec, values, *, page_endpoint, timeout_s, cwd):
        self.calls.append((spec.qualified_name, page_endpoint))
        return self.outcome


class FakeSlot:
    def __init__(self) -> None:
        self.awaiting: AwaitingUser | None = None
        self.decision = "approve"
        self.confirms: list[dict] = []
        self.holds: list[dict] = []
        self.killed = False

    @asynccontextmanager
    async def use(self):
        if self.awaiting is not None:
            raise self.awaiting
        yield "ws://127.0.0.1:1/devtools/page/T"

    def mark_killed(self) -> None:
        self.killed = True

    async def mark_awaiting_user(self, *, reason: str, instructions: str) -> str:
        self.holds.append({"reason": reason, "instructions": instructions})
        return "block"

    async def confirm(self, *, command, args, warnings, timeout_s):
        self.confirms.append({"command": command, "args": args, "warnings": warnings, "timeout_s": timeout_s})
        return self.decision


@pytest.fixture
def env(tmp_path: Path):
    source, slot = FakeSource(), FakeSlot()
    context = OpenCLIToolContext(
        source=source, catalog=CATALOG, slot=slot, pending=PendingStore(tmp_path / "pending"),
        session_id="s", member_id="", work_dir=tmp_path,
    )
    return source, slot, context, OpenCLIDescribeTool(context), OpenCLIRunTool(context)


def test_tool_cards_declare_runtime_roles(env) -> None:
    _, _, _, describe, run = env
    assert describe.card.properties["browser_runtime"]["role"] == "discovery"
    assert describe.card.idempotent is True
    assert run.card.properties["browser_runtime"] == {"role": "action", "windowed": True, "inline_limit_chars": 8000}
    assert run.card.idempotent is False and run.card.parallel_safe is False
    assert OpenCLIRunTool.accepts_tool_callback_context is True


async def test_read_ok_returns_rows_and_evidence(env) -> None:
    source, _, _, _, run = env
    output = await run.invoke({"site": "demo", "command": "search", "args": {"query": "gpu"}})
    assert output.success is True
    data = output.data
    assert data["reason"] == "ok" and data["observed_count"] == 1
    assert data["extracted"] == {"title": "t", "url": "u"}
    # Every row is reported as row-level evidence, not only the first.
    assert data["records"] == [{"title": "t", "url": "u"}]
    assert "executed" not in data and "status" not in data
    assert source.calls == [("demo/search", "ws://127.0.0.1:1/devtools/page/T")]
    assert "ws://" not in run.render_for_llm(output)


async def test_browser_free_command_never_takes_the_page(env) -> None:
    source, slot, _, _, run = env
    slot.awaiting = AwaitingUser("captcha", "wait")
    output = await run.invoke({"site": "api", "command": "top"})
    assert output.success is True
    assert source.calls == [("api/top", None)]


async def test_read_empty_is_a_normal_result(env) -> None:
    source, _, _, _, run = env
    source.outcome = RunOutcome(started=True, category="empty", rows=[], exit_code=66)
    output = await run.invoke({"site": "demo", "command": "search", "args": {"query": "x"}})
    assert output.success is True and output.data["reason"] == "empty"


async def test_needs_user_holds_the_page_and_asks_the_user(env) -> None:
    source, slot, _, _, run = env
    source.outcome = RunOutcome(started=True, category="needs_user", exit_code=77,
                                error_code="AUTH_REQUIRED", error_message="captcha required",
                                error_help="Please open Chrome or Chromium and log in")
    output = await run.invoke({"site": "demo", "command": "search", "args": {"query": "x"}})
    assert output.success is False
    assert output.data["user_action_required"]["reason"] == "captcha"
    assert "已完成，继续" in output.data["user_action_required"]["instructions"]
    assert "Chrome" not in output.data["user_action_required"]["instructions"]
    assert slot.holds and slot.holds[0]["reason"] == "captcha"


async def test_waiting_page_is_not_used_by_another_task(env) -> None:
    source, slot, _, _, run = env
    slot.awaiting = AwaitingUser("captcha", "click done")
    output = await run.invoke({"site": "demo", "command": "search", "args": {"query": "x"}})
    assert output.data["reason"] == "needs_user"
    assert output.data["user_action_required"] == {"reason": "captcha", "instructions": "click done"}
    assert source.calls == []


async def test_write_requires_confirmation(env) -> None:
    source, slot, _, _, run = env
    slot.decision = "reject"
    output = await run.invoke({"site": "demo", "command": "follow", "args": {"uid": "1"}})
    assert output.data["reason"] == "not_confirmed" and output.data["executed"] == "no"
    assert source.calls == []
    assert slot.confirms[0]["command"] == "demo follow" and slot.confirms[0]["args"] == ["uid=1"]
    slot.decision = "approve"
    output = await run.invoke({"site": "demo", "command": "follow", "args": {"uid": "1"}})
    assert output.data["executed"] == "yes" and output.success is True


@pytest.mark.parametrize("outcome", [
    RunOutcome(started=True, category="timeout", killed=True),
    RunOutcome(started=True, category="empty", rows=[], exit_code=66),
    RunOutcome(started=True, category="invalid_args", exit_code=2),
])
async def test_started_write_without_clean_exit_is_unknown_and_recorded(env, outcome) -> None:
    source, slot, context, describe, run = env
    source.outcome = outcome
    output = await run.invoke({"site": "demo", "command": "follow", "args": {"uid": "7"}})
    assert output.data["executed"] == "unknown"
    assert slot.killed is outcome.killed
    listed = await describe.invoke({"site": "demo"})
    assert listed.data["pending_writes"][0]["command"] == "demo/follow"
    # The next confirmation warns the user, and approving clears the record.
    source.outcome = RunOutcome(started=True, category="ok", rows=[], exit_code=0)
    await run.invoke({"site": "demo", "command": "follow", "args": {"uid": "7"}})
    assert slot.confirms[-1]["warnings"]
    assert context.pending.find(session_id="s", member_id="", site="demo") == []


async def test_write_that_never_started_is_not_recorded(env) -> None:
    source, _, context, _, run = env
    source.outcome = RunOutcome(started=False, category="env_unavailable")
    output = await run.invoke({"site": "demo", "command": "follow", "args": {"uid": "1"}})
    assert output.data["executed"] == "no"
    assert context.pending.find(session_id="s", member_id="", site="demo") == []


@pytest.mark.parametrize("started", [True, False])
async def test_cancelled_write_is_recorded_only_after_start_and_cancellation_propagates(env, started) -> None:
    source, slot, context, _, run = env

    async def cancel(*args, **kwargs):
        raise CommandCancelled(RunOutcome(started=started, category="error", killed=started,
                                          error_code="CANCELLED", error_message="cancelled"))

    source.run = cancel
    with pytest.raises(asyncio.CancelledError):
        await run.invoke({"site": "demo", "command": "follow", "args": {"uid": "1"}})
    assert slot.killed is started
    records = context.pending.find(session_id="s", member_id="", site="demo")
    assert len(records) == int(started)


async def test_confirmation_time_is_deducted_before_starting_a_write(env, monkeypatch) -> None:
    source, _, _, _, run = env
    remaining = iter([60.0, 0.0])
    monkeypatch.setattr("jiuwenswarm.extensions.opencli.tools._remaining_time", lambda _: next(remaining))
    result = await run.invoke({"site": "demo", "command": "follow", "args": {"uid": "1"}})
    assert (result.data["reason"], result.data["executed"]) == ("timeout", "no")
    assert not source.calls


async def test_invalid_arguments_never_run(env) -> None:
    source, _, _, _, run = env
    output = await run.invoke({"site": "demo", "command": "search", "args": {"query": "x", "site-session": "p"}})
    assert output.data["reason"] == "invalid_args"
    assert (await run.invoke({"site": "demo", "command": "nope"})).success is False
    assert source.calls == []


async def test_describe_lists_commands_and_arguments(env) -> None:
    _, _, _, describe, _ = env
    site = await describe.invoke({"site": "demo"})
    assert [c["command"] for c in site.data["commands"]] == ["follow", "search"]
    # One site-level call carries every command's arguments, so no per-command round trip is needed.
    search = next(c for c in site.data["commands"] if c["command"] == "search")
    assert search["args"][0] == {"name": "query", "required": True, "positional": True}
    assert all("args" in command for command in site.data["commands"])
    detail = await describe.invoke({"site": "demo", "command": "search"})
    assert detail.data["args"][0] == {"name": "query", "type": "str", "required": True, "positional": True}
    assert (await describe.invoke({"site": "unknown"})).success is False


@pytest.mark.parametrize("cell", ['"quoted", "json"', "中文内容" * 3, "plain text"])
def test_fitted_result_stays_recallable(cell: str) -> None:
    rows = [{"id": index, "text": cell * 40} for index in range(40_000)]
    fitted = fit_result({"ok": True, "reason": "ok", "data": rows})
    assert fitted["truncated"] is True and fitted["returned_rows"] < fitted["total_rows"]
    rendered = json.dumps(fitted, ensure_ascii=False, separators=(",", ":"))
    # Same serialisation as the offload file written by the context processor.
    stored = json.dumps({"offload_handle": "x" * 32, "messages": [{"role": "tool", "content": rendered}]},
                        ensure_ascii=False, indent=2).encode("utf-8")
    assert len(stored) < 8 * 1024 * 1024
    assert len(json.dumps(rendered, ensure_ascii=False).encode("utf-8")) <= RESULT_LIMIT_BYTES


def test_records_cover_every_row_with_scalar_fields() -> None:
    from jiuwenswarm.extensions.opencli.tools import _records

    rows = [{"title": "a", "url": "u1", "tags": ["x"]}, {"title": "b", "url": "u2"}, "not-a-row", {"title": ""}]
    assert _records(rows) == [{"title": "a", "url": "u1"}, {"title": "b", "url": "u2"}]
    assert len(_records([{"title": str(i)} for i in range(50)])) == 20
