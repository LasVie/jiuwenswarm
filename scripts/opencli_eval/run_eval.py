#!/usr/bin/env python
# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Drive the running desktop app through the M4 task set (WP11).

Each task runs in a fresh Single Agent chat, once per arm:

* ``browser``: OpenCLI off, the Browser Agent only has page tools;
* ``hybrid``:  OpenCLI on.

The app must be running (OpenCLI needs the built-in Electron browser). The
script talks to the gateway exactly like the web UI, toggles ``opencli.enabled``
between arms, restores the original setting at the end, and appends one line
per run to ``manifest.jsonl``. ``report.py`` turns the manifest plus the stored
session histories into the evaluation report.

Example::

    uv run python scripts/opencli_eval/run_eval.py --runs 2
    uv run python scripts/opencli_eval/run_eval.py --tasks hit-bilibili-hot --arms hybrid --runs 1
"""

from __future__ import annotations

import argparse
import asyncio
import itertools
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import websockets

HERE = Path(__file__).resolve().parent
MODE = "agent.work.normal"
_PREFIX_CN = "请使用浏览器完成这个任务："
_PREFIX_EN = "Use the browser to complete this task: "


def task_prompt(task: dict[str, Any]) -> str:
    """Prompt as sent; via_browser tasks ask for the browser so both arms use the Browser Agent."""
    prompt = task["prompt"]
    if not task.get("via_browser", True):
        return prompt
    has_cjk = any("\u4e00" <= char <= "\u9fff" for char in prompt)
    return (_PREFIX_CN if has_cjk else _PREFIX_EN) + prompt
ARMS = {"browser": False, "hybrid": True}


class Gateway:
    """Minimal client for the web UI's request/response/event protocol."""

    def __init__(self, ws: Any) -> None:
        self._ws = ws
        self._ids = itertools.count(1)
        self._pending: dict[str, asyncio.Future] = {}
        self.events: asyncio.Queue = asyncio.Queue()
        self._reader = asyncio.create_task(self._read())

    async def _read(self) -> None:
        async for raw in self._ws:
            try:
                frame = json.loads(raw)
            except ValueError:
                continue
            if frame.get("type") == "res" and frame.get("id") in self._pending:
                self._pending.pop(frame["id"]).set_result(frame)
            elif frame.get("type") == "event":
                await self.events.put(frame)

    async def call(self, method: str, params: dict[str, Any], timeout: float = 60.0) -> dict[str, Any]:
        request_id = f"eval_{int(time.time() * 1000):x}_{next(self._ids)}"
        future = asyncio.get_running_loop().create_future()
        self._pending[request_id] = future
        await self._ws.send(json.dumps({"type": "req", "id": request_id, "method": method, "params": params}))
        frame = await asyncio.wait_for(future, timeout)
        if not frame.get("ok"):
            raise RuntimeError(f"{method} failed: {frame.get('error') or frame}")
        return frame.get("payload") or {}

    def drain(self) -> None:
        while not self.events.empty():
            self.events.get_nowait()

    async def close(self) -> None:
        self._reader.cancel()
        await self._ws.close()


async def set_opencli(gateway: Gateway, enabled: bool) -> None:
    await gateway.call("path.set", {"opencli": {"enabled": enabled}})
    await asyncio.sleep(3)  # the agent runtime reloads its config on the next build


async def current_opencli(gateway: Gateway) -> bool | None:
    try:
        payload = await gateway.call("path.get", {})
    except (RuntimeError, asyncio.TimeoutError):
        return None
    options = payload.get("opencli") if isinstance(payload, dict) else None
    return options.get("enabled") if isinstance(options, dict) else None


async def run_task(gateway: Gateway, task: dict[str, Any], arm: str, run: int, args: argparse.Namespace) -> dict:
    gateway.drain()
    created = await gateway.call("session.create", {
        "create_token": str(uuid.uuid4()), "mode": MODE, "is_swarm": False, "work_mode": "work",
        "title": f"m4-{arm}-{task['id']}-{run}", "persist_session": False,
    })
    session_id = created.get("session_id") or created.get("sessionId")
    started = time.time()
    await gateway.call("chat.send", {
        "session_id": session_id, "content": task_prompt(task), "mode": MODE, "work_mode": "work",
        "skills": [], "enable_swarmflow": False,
    })
    record = {"task": task["id"], "group": task["group"], "arm": arm, "run": run, "session_id": session_id,
              "started_at": started, "timed_out": False, "asked_user": None, "error": None}
    finished_at = None
    deadline = started + args.timeout
    while True:
        wait = (finished_at + args.quiet - time.time()) if finished_at else (deadline - time.time())
        if wait <= 0:
            record["timed_out"] = finished_at is None
            break
        try:
            frame = await asyncio.wait_for(gateway.events.get(), timeout=wait)
        except asyncio.TimeoutError:
            continue
        event, payload = frame.get("event"), frame.get("payload") or {}
        if payload.get("session_id") not in (None, session_id):
            continue
        if event == "chat.processing_status":
            finished_at = None if payload.get("is_processing") else time.time()
        elif event in ("chat.subagent_activity", "chat.subtask_update") and finished_at:
            finished_at = time.time()  # sub-agent work still reporting; extend the quiet window
        elif event in ("chat.ask_user_question", "plan.approval_required"):
            record["asked_user"] = str(payload.get("source") or event)
            break  # an unattended run cannot answer; the report counts it as blocked
        elif event in ("chat.error", "execution.error") and payload.get("session_id") == session_id:
            record["error"] = str(payload.get("message") or payload.get("error") or payload)[:300]
    record["finished_at"] = finished_at or time.time()
    record["wall_s"] = round(record["finished_at"] - started, 1)
    return record


async def main_async(args: argparse.Namespace) -> Path:
    tasks = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))["tasks"]
    if args.tasks:
        wanted = set(args.tasks.split(","))
        tasks = [task for task in tasks if task["id"] in wanted]
    out_dir = Path(args.out) / datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = out_dir / "manifest.jsonl"
    # The gateway can be busy right after the app starts; allow a slow handshake.
    gateway = Gateway(await websockets.connect(args.ws, max_size=None, open_timeout=180, origin=args.origin))
    original = await current_opencli(gateway)
    try:
        for arm in args.arms.split(","):
            await set_opencli(gateway, ARMS[arm])
            for task, run in itertools.product(tasks, range(1, args.runs + 1)):
                print(f"[{arm}] {task['id']} run {run} ...", flush=True)
                try:
                    record = await run_task(gateway, task, arm, run, args)
                except (RuntimeError, asyncio.TimeoutError, websockets.WebSocketException) as exc:
                    record = {"task": task["id"], "group": task["group"], "arm": arm, "run": run, "error": str(exc)}
                with manifest.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                print(f"    -> {record.get('session_id')} {record.get('wall_s')}s"
                      f"{' TIMEOUT' if record.get('timed_out') else ''}{' ERROR' if record.get('error') else ''}",
                      flush=True)
    finally:
        if original is not None:
            await set_opencli(gateway, bool(original))
        await gateway.close()
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ws", default="ws://127.0.0.1:19000/ws", help="gateway WebChannel (the web UI's endpoint)")
    parser.add_argument("--origin", default="http://127.0.0.1:5173", help="Origin header, as sent by the web UI")
    parser.add_argument("--arms", default="browser,hybrid")
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--tasks", default="", help="comma-separated task ids (default: all)")
    parser.add_argument("--timeout", type=float, default=900.0, help="seconds per task")
    parser.add_argument("--quiet", type=float, default=15.0, help="seconds without events after the turn ends")
    parser.add_argument("--out", default=str(HERE / "runs"))
    manifest = asyncio.run(main_async(parser.parse_args()))
    print(f"manifest: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
