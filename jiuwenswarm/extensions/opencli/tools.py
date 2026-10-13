# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""``opencli_describe`` and ``opencli_run``: the Browser Agent's site-command tools.

The model only ever supplies a site, a command and business arguments. Every
runtime-control flag, the page binding, confirmation and outcome
classification are owned here, so none of them can be overridden by a prompt.
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncIterator, Mapping

from openjiuwen.core.foundation.tool import Tool, ToolCard
from openjiuwen.harness.tools.base_tool import ToolOutput

from jiuwenswarm.extensions.opencli.catalog import (
    ArgumentValidationError,
    Catalog,
    CommandCancelled,
    CommandSource,
    CommandSpec,
    RunOutcome,
)
from jiuwenswarm.extensions.opencli.pending import PendingStore
from jiuwenswarm.extensions.opencli.worker_page import AwaitingUser, HostError, PageSlot

try:  # Provided by agent-core's external-tool contract (C1).
    from openjiuwen.harness.tools.browser_move.playwright_runtime import browser_remaining_time
except ImportError:  # pragma: no cover - older agent-core without C1
    browser_remaining_time = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

DESCRIBE_TOOL_NAME = "opencli_describe"
RUN_TOOL_NAME = "opencli_run"
# Upstream's own browser command timeout is 60s; leave room for connect and
# pre-navigation so its structured timeout error normally wins.
COMMAND_TIMEOUT_S = 120.0
CONFIRM_TIMEOUT_S = 90.0
MIN_COMMAND_TIMEOUT_S = 15.0
MIN_CONFIRM_TIMEOUT_S = 15.0
COMMAND_MARGIN_S = 10.0
CONFIRM_MARGIN_S = 30.0
# The offload file is capped at 8 MB by browser_recall_offload; the result is
# stored there as an escaped JSON string plus an envelope, so keep 1 MiB spare.
RESULT_LIMIT_BYTES = 7 * 1024 * 1024
INLINE_LIMIT_CHARS = 8000
_EXTRACTED_FIELD_LIMIT = 20
_CAPTCHA_MARKERS = ("captcha", "验证码", "verify", "human", "安全验证", "人机")


def _text(language: str, cn: str, en: str) -> str:
    return en if language == "en" else cn


@dataclass
class OpenCLIToolContext:
    """Everything the tools need, bound when the Browser Agent spec is built."""

    source: CommandSource
    catalog: Catalog
    slot: PageSlot | None
    pending: PendingStore
    session_id: str
    member_id: str
    work_dir: Path
    language: str = "cn"
    command_timeout_s: float = COMMAND_TIMEOUT_S
    confirm_timeout_s: float = CONFIRM_TIMEOUT_S
    extra: dict[str, Any] = field(default_factory=dict)


def _remaining_time(kwargs: Mapping[str, Any]) -> float | None:
    callback_context = kwargs.get("_tool_callback_context")
    if callback_context is None or browser_remaining_time is None:
        return None
    try:
        remaining = browser_remaining_time(callback_context)
    except Exception:  # noqa: BLE001 - timing is advisory
        logger.debug("[opencli] remaining time unavailable", exc_info=True)
        return None
    return float(remaining) if remaining is not None else None


def _bounded(default_s: float, remaining_s: float | None, margin_s: float, minimum_s: float) -> float:
    if remaining_s is None:
        return default_s
    return max(minimum_s, min(default_s, remaining_s - margin_s))


def _escaped_size(value: Any) -> int:
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)
    return len(json.dumps(text, ensure_ascii=False).encode("utf-8"))


def fit_result(result: dict[str, Any], limit_bytes: int = RESULT_LIMIT_BYTES) -> dict[str, Any]:
    """Truncate ``data`` by whole rows so the stored result stays recallable."""
    if _escaped_size(result) <= limit_bytes:
        return result
    data = result.get("data")
    if isinstance(data, list):
        low, high = 0, len(data)
        while low < high:
            middle = (low + high + 1) // 2
            candidate = {**result, "data": data[:middle]}
            if _escaped_size(candidate) <= limit_bytes:
                low = middle
            else:
                high = middle - 1
        return {**result, "data": data[:low], "truncated": True, "total_rows": len(data), "returned_rows": low}
    text = json.dumps(data, ensure_ascii=False, default=str)
    keep = max(0, limit_bytes // 4)
    return {**result, "data": text[:keep], "truncated": True}


def _extracted(rows: Any) -> dict[str, str]:
    first = rows[0] if isinstance(rows, list) and rows else rows
    if not isinstance(first, dict):
        return {}
    extracted: dict[str, str] = {}
    for key, value in first.items():
        if isinstance(value, (str, int, float)) and not isinstance(value, bool) and str(value).strip():
            extracted[str(key)] = str(value)[:300]
        if len(extracted) >= _EXTRACTED_FIELD_LIMIT:
            break
    return extracted


def _row_count(rows: Any) -> int:
    if isinstance(rows, list):
        return len(rows)
    return 1 if rows not in (None, {}, []) else 0


def _user_action_reason(outcome: RunOutcome) -> str:
    if outcome.error_code == "LOGIN_WALL":
        return "user_intervention_required"
    text = f"{outcome.error_message} {outcome.error_help}".lower()
    if any(marker in text for marker in _CAPTCHA_MARKERS):
        return "captcha"
    return "login_required"


def _instructions(language: str, reason: str, needs_browser: bool) -> str:
    action = {
        "captcha": _text(language, "完成验证码或人机验证", "complete the captcha or human verification"),
        "login_required": _text(language, "登录该网站", "sign in to the site"),
    }.get(reason, _text(language, "完成页面上的安全验证", "complete the security check on the page"))
    if needs_browser:
        text = _text(
            language,
            f"请在侧栏「OpenCLI」标签页{action}，然后点击「已完成，继续」。",
            f"In the sidebar's OpenCLI tab, {action}, then click \"Done, continue\".",
        )
    else:
        text = _text(
            language,
            f"请在内置浏览器中{action}，完成后回复继续。",
            f"Please {action} in the built-in browser, then reply to continue.",
        )
    # Upstream guidance assumes an external Chrome/extension setup. The user
    # must act in the same built-in profile, so keep the product instructions.
    return text


def _render(output: ToolOutput) -> str:
    payload = output.data if isinstance(output.data, dict) else {"result": output.data}
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)


class OpenCLIDescribeTool(Tool):
    """Read-only catalog lookup; never starts a process or touches a page."""

    def __init__(self, context: OpenCLIToolContext) -> None:
        language = context.language
        super().__init__(
            ToolCard(
                name=DESCRIBE_TOOL_NAME,
                description=_text(
                    language,
                    "查看站点命令：只给 site 返回该站点的命令列表（含读/写类型和待核实的写操作）；"
                    "同时给 command 返回参数定义和输出列。不会执行任何命令。",
                    "Look up site commands: with only site, list the site's commands (read/write and "
                    "unverified writes); with command too, return its arguments and output columns. "
                    "Never executes anything.",
                ),
                input_params={
                    "type": "object",
                    "properties": {
                        "site": {"type": "string", "description": "Site name from the site list."},
                        "command": {"type": "string", "description": "Optional command name."},
                    },
                    "required": ["site"],
                },
                idempotent=True,
                properties={"browser_runtime": {"role": "discovery"}},
            )
        )
        self._context = context

    def render_for_llm(self, output: Any) -> str:
        return _render(output) if isinstance(output, ToolOutput) else str(output)

    async def invoke(self, inputs: Mapping[str, Any], **kwargs: Any) -> ToolOutput:
        context = self._context
        site = str((inputs or {}).get("site") or "").strip()
        command = str((inputs or {}).get("command") or "").strip()
        specs = context.catalog.site_commands(site)
        if not specs:
            return ToolOutput(
                success=False,
                data={"ok": False, "site": site},
                error=_text(context.language, f"站点 {site!r} 没有可用命令，请改用页面工具。",
                            f"No commands for site {site!r}; use the page tools instead."),
            )
        pending = context.pending.find(
            session_id=context.session_id, member_id=context.member_id, site=site, command=command or None
        )
        if command:
            spec = context.catalog.get(site, command)
            if spec is None:
                return ToolOutput(
                    success=False,
                    data={"ok": False, "site": site, "commands": [s.command for s in specs]},
                    error=_text(context.language, f"{site} 没有命令 {command!r}。", f"{site} has no command {command!r}."),
                )
            data: dict[str, Any] = {"ok": True, **spec.describe()}
        else:
            data = {"ok": True, "site": site, "commands": [spec.summary() for spec in specs]}
        if pending:
            data["pending_writes"] = [record.public() for record in pending]
            data["pending_note"] = _text(
                context.language,
                "这些写操作结果不明，执行同类操作前先用读命令或页面核实。",
                "These writes have unknown outcomes; verify with a read command or the page before repeating them.",
            )
        return ToolOutput(success=True, data=data)

    async def stream(self, inputs: Mapping[str, Any], **kwargs: Any) -> AsyncIterator[ToolOutput]:
        yield await self.invoke(inputs, **kwargs)


class OpenCLIRunTool(Tool):
    """Run one catalog command against the worker page."""

    # AbilityManager only forwards the callback context (remaining time) to
    # tools that opt in.
    accepts_tool_callback_context = True

    def __init__(self, context: OpenCLIToolContext) -> None:
        language = context.language
        super().__init__(
            ToolCard(
                name=RUN_TOOL_NAME,
                description=_text(
                    language,
                    "执行一条站点命令。args 按参数名传值（先用 opencli_describe 查参数）。写命令会先请用户在侧栏确认。"
                    "结果中的 reason 说明下一步：ok/empty 直接使用；needs_user 表示需要用户处理，应结束任务；"
                    "写命令 executed=unknown 时必须先核实，不得重试。",
                    "Run one site command. Pass args by name (read them with opencli_describe first). Write "
                    "commands are confirmed by the user in the sidebar first. The result's reason tells the next "
                    "step: use ok/empty directly; needs_user means the user must act, so end the task; for a "
                    "write with executed=unknown, verify first and never retry.",
                ),
                input_params={
                    "type": "object",
                    "properties": {
                        "site": {"type": "string", "description": "Site name."},
                        "command": {"type": "string", "description": "Command name."},
                        "args": {
                            "type": "object",
                            "description": "Business arguments keyed by argument name.",
                            "additionalProperties": True,
                        },
                    },
                    "required": ["site", "command"],
                },
                idempotent=False,
                parallel_safe=False,
                properties={
                    "browser_runtime": {
                        "role": "action",
                        "windowed": True,
                        "inline_limit_chars": INLINE_LIMIT_CHARS,
                    }
                },
            )
        )
        self._context = context

    def render_for_llm(self, output: Any) -> str:
        return _render(output) if isinstance(output, ToolOutput) else str(output)

    async def stream(self, inputs: Mapping[str, Any], **kwargs: Any) -> AsyncIterator[ToolOutput]:
        yield await self.invoke(inputs, **kwargs)

    def _result(self, spec: CommandSpec, *, reason: str, executed: str | None, **extra: Any) -> ToolOutput:
        ok = reason in {"ok", "empty"}
        data: dict[str, Any] = {"ok": ok, "reason": reason}
        if spec.access == "write" and executed is not None:
            data["executed"] = executed
        data["source"] = {"provider": spec.source, "command": spec.qualified_name}
        error = extra.pop("error", None)
        data.update({key: value for key, value in extra.items() if value is not None})
        if not ok and error:
            data["error"] = error
        data = fit_result(data)
        return ToolOutput(success=ok, data=data, error=None if ok else (error or reason))

    async def invoke(self, inputs: Mapping[str, Any], **kwargs: Any) -> ToolOutput:
        context = self._context
        language = context.language
        site = str((inputs or {}).get("site") or "").strip()
        command = str((inputs or {}).get("command") or "").strip()
        raw_args = (inputs or {}).get("args") or {}
        spec = context.catalog.get(site, command)
        if spec is None:
            return ToolOutput(
                success=False,
                data={"ok": False, "reason": "invalid_args"},
                error=_text(language, f"没有命令 {site}/{command}，先用 opencli_describe 查看。",
                            f"No command {site}/{command}; call opencli_describe first."),
            )
        if not isinstance(raw_args, Mapping):
            return self._result(spec, reason="invalid_args", executed="no", error="args must be an object")
        try:
            values = spec.normalize_args(raw_args)
        except ArgumentValidationError as exc:
            return self._result(spec, reason="invalid_args", executed="no", error=str(exc))

        remaining = _remaining_time(kwargs)
        if spec.access == "write":
            decision = await self._confirm(spec, values, raw_args, remaining)
            if decision != "approve":
                message = {
                    "reject": _text(language, "用户拒绝执行该写操作。", "The user rejected this write."),
                    "unavailable": _text(language, "无法显示确认条，未执行。", "Confirmation unavailable; not executed."),
                }.get(decision, _text(language, "确认超时，未执行。", "Confirmation timed out; not executed."))
                return self._result(spec, reason="not_confirmed", executed="no", error=message)

        # Confirmation consumes the same task budget as execution.
        remaining = _remaining_time(kwargs)
        if remaining is not None and remaining < COMMAND_MARGIN_S + MIN_COMMAND_TIMEOUT_S:
            return self._result(spec, reason="timeout", executed="no",
                                error=_text(language, "任务剩余时间不足，未启动命令。",
                                            "Insufficient task time remaining; command not started."))
        timeout_s = _bounded(context.command_timeout_s, remaining, COMMAND_MARGIN_S, MIN_COMMAND_TIMEOUT_S)
        if not spec.needs_browser:
            outcome = await self._run_command(spec, values, raw_args, None, timeout_s, None)
            return await self._finish(spec, raw_args, outcome, slot=None)
        if context.slot is None:
            return self._result(spec, reason="env_unavailable", executed="no",
                                error=_text(language, "内置浏览器不可用。", "The built-in browser is unavailable."))
        try:
            async with context.slot.use() as endpoint:
                remaining = _remaining_time(kwargs)
                if remaining is not None and remaining < COMMAND_MARGIN_S + MIN_COMMAND_TIMEOUT_S:
                    return self._result(spec, reason="timeout", executed="no",
                                        error=_text(language, "任务剩余时间不足，未启动命令。",
                                                    "Insufficient task time remaining; command not started."))
                timeout_s = _bounded(context.command_timeout_s, remaining, COMMAND_MARGIN_S, MIN_COMMAND_TIMEOUT_S)
                outcome = await self._run_command(spec, values, raw_args, endpoint, timeout_s, context.slot)
                if outcome.killed:
                    context.slot.mark_killed()
                return await self._finish(spec, raw_args, outcome, slot=context.slot)
        except AwaitingUser as waiting:
            return self._result(
                spec,
                reason="needs_user",
                executed="no",
                error=waiting.instructions or waiting.reason,
                user_action_required={
                    "reason": waiting.reason or "user_intervention_required",
                    "instructions": waiting.instructions,
                },
            )
        except HostError as exc:
            return self._result(spec, reason="env_unavailable", executed="no", error=str(exc))

    async def _run_command(
        self, spec: CommandSpec, values: list, raw_args: Mapping[str, Any],
        endpoint: str | None, timeout_s: float, slot: PageSlot | None,
    ) -> RunOutcome:
        context = self._context
        try:
            return await context.source.run(
                spec, values, page_endpoint=endpoint, timeout_s=timeout_s, cwd=context.work_dir
            )
        except CommandCancelled as exc:
            if exc.outcome.killed and slot is not None:
                slot.mark_killed()
            # A started write remains uncertain even though no tool result will
            # be delivered to the cancelled agent. Persist it before unwinding.
            cleanup = asyncio.create_task(self._finish(spec, raw_args, exc.outcome, slot=slot))
            while not cleanup.done():
                try:
                    await asyncio.shield(cleanup)
                except asyncio.CancelledError:
                    continue
            cleanup.result()
            raise

    async def _confirm(
        self, spec: CommandSpec, values: list, raw_args: Mapping[str, Any], remaining: float | None
    ) -> str:
        context = self._context
        if context.slot is None:
            return "unavailable"
        pending = context.pending.find(
            session_id=context.session_id, member_id=context.member_id, site=spec.site, command=spec.command
        )
        warnings = [
            _text(
                context.language,
                f"该操作之前结果不明（{record.public()['created_at']}，参数 {record.args_preview}），可能已经生效。",
                f"A previous run had an unknown outcome ({record.public()['created_at']}, args "
                f"{record.args_preview}); it may already have taken effect.",
            )
            for record in pending
        ]
        timeout_s = _bounded(context.confirm_timeout_s, remaining, CONFIRM_MARGIN_S, MIN_CONFIRM_TIMEOUT_S)
        try:
            decision = await context.slot.confirm(
                command=f"{spec.site} {spec.command}",
                args=[f"{arg.name}={text}" for arg, text in values],
                warnings=warnings,
                timeout_s=timeout_s,
            )
        except HostError:
            logger.warning("[opencli] confirmation request failed", exc_info=True)
            return "unavailable"
        except AwaitingUser:
            return "unavailable"
        if decision == "approve" and pending:
            context.pending.clear(session_id=context.session_id, record_ids=[record.id for record in pending])
        return decision

    async def _finish(
        self, spec: CommandSpec, raw_args: Mapping[str, Any], outcome: RunOutcome, *, slot: PageSlot | None
    ) -> ToolOutput:
        context = self._context
        category = outcome.category
        executed = "no" if not outcome.started else ("yes" if outcome.exit_code == 0 else "unknown")
        if spec.access == "write" and executed == "unknown":
            context.pending.add(
                session_id=context.session_id,
                member_id=context.member_id,
                site=spec.site,
                command=spec.command,
                args=raw_args,
                reason=category,
            )
        if category in {"ok", "empty"} and outcome.exit_code == 0:
            rows = outcome.rows if outcome.rows is not None else []
            count = _row_count(rows)
            extracted = _extracted(rows)
            provenance = {key: {"source": f"{spec.source}:{spec.qualified_name}"} for key in extracted}
            return self._result(
                spec,
                reason=category,
                executed=executed,
                data=rows,
                observed_count=count,
                extracted=extracted or None,
                field_provenance=provenance or None,
            )
        message = outcome.error_message or category
        if outcome.error_help:
            message = f"{message} ({outcome.error_help})"
        if category == "needs_user":
            reason = _user_action_reason(outcome)
            instructions = _instructions(context.language, reason, spec.needs_browser)
            if slot is not None:
                try:
                    await slot.mark_awaiting_user(reason=reason, instructions=instructions)
                except HostError:
                    logger.warning("[opencli] failed to hold the worker page for the user", exc_info=True)
            return self._result(
                spec,
                reason="needs_user",
                executed=executed,
                error=outcome.error_message or instructions,
                user_action_required={"reason": reason, "instructions": instructions},
            )
        return self._result(
            spec,
            reason=category,
            executed=executed,
            error=message,
            error_code=outcome.error_code or None,
        )


def build_tools(context: OpenCLIToolContext) -> list[Tool]:
    return [OpenCLIDescribeTool(context), OpenCLIRunTool(context)]
