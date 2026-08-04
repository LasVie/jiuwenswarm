# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

from __future__ import annotations

import os
import sys

import pytest

from jiuwenswarm.agents.harness.common.tools.bash_tool_safety import (
    _is_opencli_command,
    _pre_execute_shell_command,
    _with_opencli_utf8_options,
    _wrap_shell_execute_cmd,
    _wrap_shell_execute_cmd_stream,
    install_shell_tool_safety_hooks,
    reset_installed_flag,
)


@pytest.fixture(autouse=True)
def _reset_install_flag():
    reset_installed_flag()
    yield
    reset_installed_flag()


def test_pre_execute_blocks_pkill_on_jiuwenswarm_tui() -> None:
    err = _pre_execute_shell_command('pkill -f "jiuwenswarm-tui" 2>/dev/null')
    assert err is not None
    assert "rejected for safety" in err


def test_pre_execute_allows_unrelated_ps() -> None:
    err = _pre_execute_shell_command("ps aux | grep node | head -5")
    assert err is None


@pytest.mark.parametrize(
    "command",
    [
        "opencli xiaohongshu search test",
        "opencli.cmd xiaohongshu whoami",
        '"C:\\Tools\\OpenCLI\\opencli.exe" xiaohongshu home-feed',
        "set FOO=bar && opencli xiaohongshu search test",
        'Get-Date; & "C:\\Tools\\OpenCLI\\opencli.cmd" xiaohongshu whoami',
        "echo ready | opencli xiaohongshu whoami",
    ],
)
def test_detects_opencli_executable(command: str) -> None:
    assert _is_opencli_command(command)


@pytest.mark.parametrize(
    "command",
    [
        "opencli-helper test",
        "python opencli.py",
        "echo opencli",
        'Write-Output "opencli xiaohongshu whoami"',
        "echo opencli.md",
    ],
)
def test_does_not_match_other_executables(command: str) -> None:
    assert not _is_opencli_command(command)


def test_opencli_utf8_options_are_scoped_and_non_mutating() -> None:
    original = {"timeout": 30, "options": {"chunk_size": 512}}

    updated = _with_opencli_utf8_options("opencli xiaohongshu whoami", original)

    assert updated["options"] == {"chunk_size": 512, "encoding": "utf-8"}
    assert original == {"timeout": 30, "options": {"chunk_size": 512}}
    assert _with_opencli_utf8_options("git status", original) is original


def test_opencli_utf8_does_not_override_explicit_encoding() -> None:
    updated = _with_opencli_utf8_options(
        "opencli xiaohongshu whoami",
        {"options": {"encoding": "gbk"}},
    )

    assert updated["options"]["encoding"] == "gbk"


@pytest.mark.asyncio
async def test_execute_cmd_wrapper_injects_utf8() -> None:
    captured: dict[str, object] = {}

    async def original(self, command, *args, **kwargs):
        captured.update(kwargs)
        return "ok"

    wrapped = _wrap_shell_execute_cmd(original)
    result = await wrapped(object(), "opencli xiaohongshu whoami", timeout=30)

    assert result == "ok"
    assert captured["options"] == {"encoding": "utf-8"}


@pytest.mark.asyncio
async def test_execute_cmd_stream_wrapper_injects_utf8() -> None:
    captured: dict[str, object] = {}

    async def original(self, command, *args, **kwargs):
        captured.update(kwargs)
        yield "chunk"

    wrapped = _wrap_shell_execute_cmd_stream(original)
    chunks = [item async for item in wrapped(object(), "opencli xiaohongshu whoami")]

    assert chunks == ["chunk"]
    assert captured["options"] == {"encoding": "utf-8"}


def test_install_wraps_bash_tool_invoke() -> None:
    from openjiuwen.harness.tools.shell.bash._tool import BashTool
    from openjiuwen.core.sys_operation.local.shell_operation import ShellOperation

    install_shell_tool_safety_hooks()
    assert getattr(BashTool.invoke, "jiuwenswarm_safety_wrapped", False)
    assert getattr(
        ShellOperation.execute_cmd,
        "jiuwenswarm_opencli_utf8_wrapped",
        False,
    )
    assert getattr(
        ShellOperation.execute_cmd_stream,
        "jiuwenswarm_opencli_utf8_wrapped",
        False,
    )
    install_shell_tool_safety_hooks()
    assert getattr(BashTool.invoke, "jiuwenswarm_safety_wrapped", False)


@pytest.mark.skipif(os.name != "nt", reason="Windows code-page regression")
@pytest.mark.asyncio
async def test_opencli_shell_output_decodes_as_utf8_on_windows(
    tmp_path,
    monkeypatch,
) -> None:
    from openjiuwen.core.sys_operation.base import OperationMode
    from openjiuwen.core.sys_operation.config import LocalWorkConfig
    from openjiuwen.core.sys_operation.local.shell_operation import ShellOperation

    expected = "新加坡周末亲子活动 🇸🇬"
    payload_hex = expected.encode("utf-8").hex()
    fake_opencli = tmp_path / "opencli.cmd"
    fake_opencli.write_text(
        "@echo off\n"
        f'"{sys.executable}" -c "import sys;'
        f"sys.stdout.buffer.write(bytes.fromhex('{payload_hex}'))\"\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        ShellOperation,
        "_detect_shell_encoding",
        staticmethod(lambda: "cp1252"),
    )
    install_shell_tool_safety_hooks()
    shell = ShellOperation(
        "shell",
        OperationMode.LOCAL,
        "test",
        LocalWorkConfig(shell_allowlist=None),
    )

    result = await shell.execute_cmd(
        f'"{fake_opencli}"',
        timeout=30,
        shell_type="auto",
    )

    assert result.code == 0
    assert result.data is not None
    assert result.data.stdout == expected
    assert "\ufffd" not in result.data.stdout
