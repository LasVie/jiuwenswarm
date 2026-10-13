"""Part B of opencli_smoke.cjs: the real OpenCLI tool stack on the Electron worker page.

Started by the smoke main with SMOKE_* variables; not a pytest module.
``prepare`` materializes the bundled runtime with Electron Node and prints it;
``run`` drives ``OpenCLIRunTool`` through the real target resolver routes.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

import httpx

from jiuwenswarm.extensions.opencli.catalog import Catalog
from jiuwenswarm.extensions.opencli.pending import PendingStore
from jiuwenswarm.extensions.opencli.sources.opencli import OpenCLISource, prepare_runtime
from jiuwenswarm.extensions.opencli.tools import OpenCLIRunTool, OpenCLIToolContext
from jiuwenswarm.extensions.opencli.worker_page import HostBinding, HostClient, PageSlot

ELECTRON = os.environ.get("SMOKE_ELECTRON", "")
WORKSPACE = Path(os.environ.get("SMOKE_WORKSPACE", "."))
CONTROL = os.environ.get("SMOKE_CONTROL", "")
MEMBER = "driver"

_BROWSER = {"site": "fixture", "needs_browser": True, "domain": "127.0.0.1", "args": []}
_TEXT_ARG = [{"name": "text", "type": "str", "required": True}]
FIXTURE_COMMANDS = [
    {**_BROWSER, "command": "read", "access": "read", "columns": ["title", "rank"],
     "args": [{"name": "limit", "type": "int", "default": 3}]},
    {"site": "fixture", "command": "public", "access": "read", "needs_browser": False, "args": []},
    {**_BROWSER, "command": "write", "access": "write", "args": _TEXT_ARG},
    {**_BROWSER, "command": "write-lost", "access": "write", "args": _TEXT_ARG},
    {**_BROWSER, "command": "captcha", "access": "read"},
    {**_BROWSER, "command": "slow", "access": "read"},
    {"site": "fixture", "command": "echo", "access": "read", "needs_browser": False, "args": [
        {"name": "query", "type": "str", "required": True, "positional": True},
        {"name": "flag", "type": "boolean", "default": False},
        {"name": "limit", "type": "int", "default": 5},
        {"name": "text", "type": "str"},
    ]},
]

failures: list[str] = []


def check(check_id: str, ok: bool, detail: Any = "") -> None:
    if not ok:
        failures.append(check_id)
    text = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print(f"{'PASS' if ok else 'FAIL'} B:{check_id}{f' - {text}' if text else ''}", flush=True)


async def control(action: str, **params: str) -> dict[str, Any]:
    async with httpx.AsyncClient(trust_env=False, timeout=10) as client:
        response = await client.get(f"{CONTROL}/{action}", params=params)
        return response.json()


async def worker_view() -> dict[str, Any]:
    state = await control("state")
    return next(
        view for view in state["views"]
        if view["role"] == "opencli" and view["memberId"] == MEMBER and not view["destroyed"]
    )


def prepare() -> None:
    runtime = prepare_runtime(ELECTRON, user_workspace_dir=WORKSPACE)
    print(json.dumps({
        "cli_path": str(runtime.cli_path),
        "home_dir": str(runtime.home_dir),
        "node_version": runtime.node_version,
        "version": runtime.version,
    }))


async def run() -> int:
    runtime = prepare_runtime(ELECTRON, user_workspace_dir=WORKSPACE)
    shutil.copytree(os.environ["SMOKE_ADAPTERS"], runtime.home_dir / ".opencli" / "clis" / "fixture",
                    dirs_exist_ok=True)
    binding = HostBinding(
        resolver=os.environ["SMOKE_RESOLVER"], token=os.environ["SMOKE_TOKEN"],
        session_id="smoke", member_id=MEMBER,
    )
    work_dir = WORKSPACE / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    context = OpenCLIToolContext(
        source=OpenCLISource(runtime),
        catalog=Catalog.from_payload({"commands": FIXTURE_COMMANDS}, source="opencli"),
        slot=PageSlot(HostClient(binding), hold_ttl_s=120),
        pending=PendingStore(WORKSPACE / "pending"),
        session_id="smoke",
        member_id=MEMBER,
        work_dir=work_dir,
        language="en",
        confirm_timeout_s=15,
    )
    tool = OpenCLIRunTool(context)

    async def call(command: str, **args: Any) -> dict[str, Any]:
        output = await tool.invoke({"site": "fixture", "command": command, "args": args})
        return dict(output.data or {})

    async def posts() -> int:
        return int((await control("state"))["fixture"]["posts"])

    result = await call("read", limit=2)
    check("read-ok", result.get("reason") == "ok" and result.get("observed_count") == 2
          and result.get("extracted", {}).get("title") == "alpha", result)
    first = await worker_view()
    check("lease-released-after-command", first["url"].startswith("http://127.0.0.1")
          and first["leases"] == 0, first)

    result = await call("public")
    check("browser-free-ok", result.get("reason") == "ok" and result.get("observed_count") == 2, result)

    result = await call("echo", query="-foo bar", flag=False, limit=3, text="-x=1")
    check("dash-and-space-values-reach-adapter",
          result.get("data") == [{"query": "-foo bar", "flag": False, "limit": 3, "text": "-x=1"}], result)

    before = await posts()
    await control("confirm-mode", decision="approve")
    result = await call("write", text="hello")
    check("write-approved", result.get("reason") == "ok" and result.get("executed") == "yes"
          and await posts() == before + 1, result)

    await control("confirm-mode", decision="reject")
    result = await call("write", text="hello")
    check("write-rejected-not-run", result.get("reason") == "not_confirmed" and result.get("executed") == "no"
          and await posts() == before + 1, result)

    await control("confirm-mode", decision="approve")
    result = await call("write-lost", text="once")
    pending = context.pending.find(session_id="smoke", member_id=MEMBER, site="fixture")
    check("write-unknown-outcome-recorded", result.get("executed") == "unknown" and len(pending) == 1
          and await posts() == before + 2, {"result": result, "pending": len(pending)})
    await call("write-lost", text="twice")
    warnings = (await control("state"))["lastConfirm"]["warnings"]
    check("pending-write-warned-on-next-confirm", len(warnings) == 1, warnings)

    result = await call("captcha")
    held = await worker_view()
    check("captcha-needs-user", result.get("reason") == "needs_user"
          and result.get("user_action_required", {}).get("reason") == "captcha"
          and (held.get("hold") or {}).get("state") == "pending", {"result": result, "hold": held.get("hold")})

    result = await call("read")
    check("hold-blocks-next-command", result.get("reason") == "needs_user" and result.get("executed") is None, result)

    decided = await control("decide", panelId=held["panelId"], blockId=held["hold"]["blockId"], decision="resolved")
    result = await call("read")
    after = await worker_view()
    check("resolved-hold-keeps-page", decided.get("applied") and result.get("reason") == "ok"
          and after["targetId"] == held["targetId"] and not after.get("hold"), {"result": result["reason"]})

    await call("captcha")
    held = await worker_view()
    await control("decide", panelId=held["panelId"], blockId=held["hold"]["blockId"], decision="abandoned")
    result = await call("read")
    after = await worker_view()
    check("abandoned-hold-resets-page", result.get("reason") == "ok" and after["targetId"] != held["targetId"],
          {"before": held["targetId"], "after": after["targetId"]})

    context.command_timeout_s = 6
    before_target = after["targetId"]
    result = await call("slow")
    context.command_timeout_s = 120
    after = await worker_view()
    ticks = (await control("state"))["fixture"]["ticks"]
    await asyncio.sleep(1.5)
    ticks_later = (await control("state"))["fixture"]["ticks"]
    check("timeout-kills-and-resets-page", result.get("reason") == "timeout" and after["targetId"] != before_target
          and ticks_later == ticks, {"result": result, "ticks_after_reset": ticks_later - ticks})

    result = await call("read")
    check("read-after-reset-ok", result.get("reason") == "ok", result.get("reason"))

    await control("confirm-mode", decision="timeout")
    context.confirm_timeout_s = 5
    result = await call("write", text="late")
    check("confirm-timeout-not-run", result.get("reason") == "not_confirmed" and result.get("executed") == "no", result)
    return 1 if failures else 0


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "prepare":
        prepare()
        return 0
    return asyncio.run(run())


if __name__ == "__main__":
    sys.exit(main())
