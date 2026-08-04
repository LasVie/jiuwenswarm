# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Apply jiuwenswarm shell compatibility hooks to harness shell tools.

The agent's primary shell tool is ``bash`` (openjiuwen ``BashTool``), not
``mcp_exec_command``.  Safety checks in ``command_tools`` only affect the latter
unless we hook the harness tools here.  OpenCLI also writes UTF-8 to redirected
pipes on Windows, while OpenJiuwen's local shell operation otherwise decodes
with the system code page.  The hooks below keep that UTF-8 override scoped to
OpenCLI commands so unrelated Windows command output retains its existing
encoding policy.
"""

from __future__ import annotations

import re
from typing import Any, Awaitable, Callable

_installed = False

_OPENCLI_EXECUTABLE_RE = re.compile(
    r"""
    (?:^|(?:&&|\|\||[|;])\s*)
    (?:call\s+|&\s*)?
    (?:
        "(?:[^"]*[\\/])?opencli(?:\.(?:bat|cmd|exe|ps1))?"
        | '(?:[^']*[\\/])?opencli(?:\.(?:bat|cmd|exe|ps1))?'
        | (?:[^\s"'|&;]+[\\/])?opencli(?:\.(?:bat|cmd|exe|ps1))?
    )
    (?=$|[\s|&;<>])
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _is_opencli_command(command: str) -> bool:
    """Return whether *command* invokes an OpenCLI executable."""
    return bool(_OPENCLI_EXECUTABLE_RE.search(str(command or "")))


def _with_opencli_utf8_options(
    command: str,
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    """Inject UTF-8 decoding for OpenCLI without mutating caller arguments."""
    if not _is_opencli_command(command):
        return kwargs

    updated = dict(kwargs)
    raw_options = updated.get("options")
    options = dict(raw_options) if isinstance(raw_options, dict) else {}
    options.setdefault("encoding", "utf-8")
    updated["options"] = options
    return updated


def _pre_execute_shell_command(command: str) -> str | None:
    """Return an error string when *command* must not run; else None."""
    from openjiuwen.core.sys_operation.shell_process_registry import (
        resolve_shell_session_id,
    )

    from jiuwenswarm.agents.harness.common.tools.command_tools import (
        _check_command_safety,
        _check_worktree_path_safety,
        _enforce_tui_spawn_budget,
    )

    blocked = _check_command_safety(command)
    if blocked:
        return f"[ERROR]: command rejected for safety ({blocked})."
    worktree_block = _check_worktree_path_safety(command)
    if worktree_block:
        return f"[ERROR]: {worktree_block}"
    spawn_block = _enforce_tui_spawn_budget(command, resolve_shell_session_id() or "")
    if spawn_block:
        return f"[ERROR]: {spawn_block}"
    return None


def _wrap_invoke(
    original: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    from openjiuwen.harness.tools.base_tool import ToolOutput

    async def invoke(self: Any, inputs: dict[str, Any], **kwargs: Any) -> Any:
        parsed = getattr(self, "_parse_inputs")(inputs)
        if parsed.command:
            err = _pre_execute_shell_command(parsed.command)
            if err:
                return ToolOutput(success=False, error=err)
        return await original(self, inputs, **kwargs)

    invoke.jiuwenswarm_safety_wrapped = True
    return invoke


def _wrap_stream(
    original: Callable[..., Any],
) -> Callable[..., Any]:
    from openjiuwen.harness.tools.base_tool import ToolOutput

    async def stream(self: Any, inputs: dict[str, Any], **kwargs: Any):
        parsed = getattr(self, "_parse_inputs")(inputs)
        if parsed.command:
            err = _pre_execute_shell_command(parsed.command)
            if err:
                yield ToolOutput(success=False, error=err)
                return
        async for item in original(self, inputs, **kwargs):
            yield item

    stream.jiuwenswarm_safety_wrapped = True
    return stream


def _patch_tool_class(tool_cls: type) -> None:
    if not getattr(tool_cls.invoke, "jiuwenswarm_safety_wrapped", False):
        tool_cls.invoke = _wrap_invoke(tool_cls.invoke)
    if not getattr(tool_cls.stream, "jiuwenswarm_safety_wrapped", False):
        tool_cls.stream = _wrap_stream(tool_cls.stream)


def _wrap_shell_execute_cmd(
    original: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    async def execute_cmd(
        self: Any,
        command: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return await original(
            self,
            command,
            *args,
            **_with_opencli_utf8_options(command, kwargs),
        )

    execute_cmd.jiuwenswarm_opencli_utf8_wrapped = True
    return execute_cmd


def _wrap_shell_execute_cmd_stream(
    original: Callable[..., Any],
) -> Callable[..., Any]:
    async def execute_cmd_stream(
        self: Any,
        command: str,
        *args: Any,
        **kwargs: Any,
    ):
        async for item in original(
            self,
            command,
            *args,
            **_with_opencli_utf8_options(command, kwargs),
        ):
            yield item

    execute_cmd_stream.jiuwenswarm_opencli_utf8_wrapped = True
    return execute_cmd_stream


def _patch_local_shell_operation(shell_cls: type) -> None:
    """Patch local shell output decoding for OpenCLI commands only."""
    if not getattr(
        shell_cls.execute_cmd,
        "jiuwenswarm_opencli_utf8_wrapped",
        False,
    ):
        shell_cls.execute_cmd = _wrap_shell_execute_cmd(shell_cls.execute_cmd)
    if not getattr(
        shell_cls.execute_cmd_stream,
        "jiuwenswarm_opencli_utf8_wrapped",
        False,
    ):
        shell_cls.execute_cmd_stream = _wrap_shell_execute_cmd_stream(
            shell_cls.execute_cmd_stream
        )


def install_shell_tool_safety_hooks() -> None:
    """Idempotently wire safety and OpenCLI encoding hooks."""
    global _installed
    if _installed:
        return

    from openjiuwen.harness.tools.shell.bash._tool import BashTool
    from openjiuwen.core.sys_operation.local.shell_operation import ShellOperation

    _patch_tool_class(BashTool)
    _patch_local_shell_operation(ShellOperation)

    try:
        from openjiuwen.harness.tools.shell.powershell._tool import PowerShellTool

        _patch_tool_class(PowerShellTool)
    except ImportError:
        pass

    _installed = True


def reset_installed_flag() -> None:
    """Reset the installed flag so hooks can be re-applied (for testing)."""
    global _installed
    _installed = False


__all__ = ["install_shell_tool_safety_hooks", "reset_installed_flag"]
