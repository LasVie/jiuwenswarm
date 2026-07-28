from __future__ import annotations

import inspect
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from jiuwenswarm.agents.harness.common.opencli.executor import (
    OpenCLIExecutionError,
    OpenCLIExecutor,
)
from jiuwenswarm.agents.harness.common.opencli.executors import launcher
from jiuwenswarm.agents.harness.common.opencli.executors.manifest import (
    render_manifest_command_argv,
)
from jiuwenswarm.agents.harness.common.opencli.executors import (
    xiaohongshu_publish as wheel_publish,
)


def _generic_contract(**overrides):
    values = {
        "site": "wikipedia",
        "operation": "discovery",
        "command": "search",
        "executor": "generic_manifest_read",
        "execution_state": "enabled",
        "semantic_effect": "public_read",
        "risk": "low",
        "auth": "none",
        "transport": "public_http",
        "strategy": "public",
        "browser": False,
        "opencli_version": "1.8.6",
        "access": "read",
        "confirmation": "none",
        "file_inputs": (),
        "file_outputs": (),
        "sensitive_output": (),
        "args": (
            {
                "name": "query",
                "type": "str",
                "required": True,
                "positional": True,
                "help": "Search query",
            },
            {
                "name": "limit",
                "type": "int",
                "required": False,
                "default": 10,
                "help": "Max results",
            },
            {
                "name": "exact",
                "type": "boolean",
                "required": False,
                "default": False,
                "help": "Require an exact match",
            },
            {
                "name": "lang",
                "type": "string",
                "required": False,
                "default": "en",
                "choices": ("en", "zh"),
                "help": "Language",
            },
        ),
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def _xiaohongshu_contract(tmp_path: Path):
    return SimpleNamespace(
        site="xiaohongshu",
        operation="publishing",
        command="publish",
        executor="xiaohongshu_guarded_publish",
        opencli_version="1.8.6",
        skill_root=tmp_path / "installed-skill-does-not-contain-runtime",
    )


def test_manifest_renderer_uses_only_contract_command_and_fixed_json_format():
    argv = render_manifest_command_argv(
        _generic_contract(),
        {
            "query": "--literal search",
            "limit": 5,
            "exact": False,
            "lang": "zh",
        },
    )

    assert argv == [
        "wikipedia",
        "search",
        "--limit=5",
        "--exact=false",
        "--lang=zh",
        "-f",
        "json",
        "--",
        "--literal search",
    ]
    assert "--site" not in argv
    assert "--command" not in argv


@pytest.mark.parametrize(
    ("arguments", "expected_code"),
    [
        ({"query": "safe", "unknown": "value"}, "opencli_argument_unknown"),
        ({"query": "safe", "limit": True}, "opencli_argument_type_invalid"),
        ({"query": 123}, "opencli_argument_type_invalid"),
        ({"query": "safe", "exact": "false"}, "opencli_argument_type_invalid"),
        ({"query": "safe", "lang": "fr"}, "opencli_argument_choice_invalid"),
        ({}, "opencli_argument_required"),
        (["not", "a", "mapping"], "opencli_arguments_invalid"),
    ],
)
def test_manifest_renderer_rejects_unknown_missing_and_coerced_arguments(
    arguments,
    expected_code,
):
    with pytest.raises(OpenCLIExecutionError) as caught:
        render_manifest_command_argv(_generic_contract(), arguments)

    assert caught.value.code == expected_code
    assert caught.value.attempted is False
    assert caught.value.fallback_allowed is False


def test_manifest_renderer_enforces_reviewed_argument_constraints():
    contract = _generic_contract(
        args=(
            {
                "name": "query",
                "type": "string",
                "required": True,
                "positional": True,
                "constraints": {
                    "pattern": r"^[a-z]+$",
                    "max_length": 8,
                },
            },
            {
                "name": "limit",
                "type": "int",
                "required": True,
                "constraints": {
                    "minimum": 1,
                    "maximum": 50,
                },
            },
        )
    )

    assert render_manifest_command_argv(
        contract,
        {"query": "opencli", "limit": 50},
    ) == [
        "wikipedia",
        "search",
        "--limit=50",
        "-f",
        "json",
        "--",
        "opencli",
    ]

    for arguments, expected_code in (
        ({"query": "toolongtext", "limit": 1}, "opencli_argument_length_invalid"),
        ({"query": "OpenCLI", "limit": 1}, "opencli_argument_pattern_invalid"),
        ({"query": "opencli", "limit": 0}, "opencli_argument_range_invalid"),
        ({"query": "opencli", "limit": 51}, "opencli_argument_range_invalid"),
    ):
        with pytest.raises(OpenCLIExecutionError) as caught:
            render_manifest_command_argv(contract, arguments)
        assert caught.value.code == expected_code
        assert caught.value.attempted is False
        assert caught.value.fallback_allowed is False


def test_manifest_renderer_rejects_invalid_constraint_schema_before_dispatch():
    contract = _generic_contract(
        args=(
            {
                "name": "query",
                "type": "string",
                "required": True,
                "constraints": {"pattern": "["},
            },
        )
    )

    with pytest.raises(OpenCLIExecutionError) as caught:
        render_manifest_command_argv(contract, {"query": "safe"})

    assert caught.value.code == "opencli_manifest_arguments_invalid"
    assert caught.value.attempted is False
    assert caught.value.fallback_allowed is False


@pytest.mark.asyncio
async def test_generic_public_read_executes_shell_free_with_trusted_launcher(
    tmp_path: Path,
):
    calls: list[tuple[list[str], dict[str, object]]] = []

    def _runner(argv, **kwargs):
        calls.append((list(argv), dict(kwargs)))
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout=json.dumps([{"title": "OpenCLI"}]),
            stderr="",
        )

    trusted_launcher = [
        "C:/trusted/node.exe",
        "C:/trusted/opencli/main.js",
    ]
    executor = OpenCLIExecutor(
        process_runner=_runner,
        launcher_resolver=lambda: trusted_launcher,
        launcher_version_probe=lambda argv: (
            "1.8.6" if list(argv) == trusted_launcher else "unexpected"
        ),
    )

    result = await executor.execute(
        _generic_contract(),
        arguments={"query": "agent safety", "limit": 3},
        workspace_roots=[tmp_path],
    )

    assert result["ok"] is True
    assert result["attempted"] is True
    assert result["fallback_allowed"] is False
    assert result["result"] == [{"title": "OpenCLI"}]
    assert len(calls) == 1
    argv, options = calls[0]
    assert argv[:4] == [
        "C:/trusted/node.exe",
        "C:/trusted/opencli/main.js",
        "wikipedia",
        "search",
    ]
    assert argv[-2:] == ["--", "agent safety"]
    assert options["shell"] is False
    assert "env" not in options


@pytest.mark.asyncio
async def test_generic_command_with_no_declared_arguments_accepts_empty_object(
    tmp_path: Path,
):
    calls: list[list[str]] = []

    def _runner(argv, **kwargs):
        calls.append(list(argv))
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout="{}",
            stderr="",
        )

    executor = OpenCLIExecutor(
        process_runner=_runner,
        launcher_resolver=lambda: [
            "C:/trusted/node.exe",
            "C:/trusted/opencli/main.js",
        ],
        launcher_version_probe=lambda _argv: "1.8.6",
    )

    result = await executor.execute(
        _generic_contract(args=()),
        arguments={},
        workspace_roots=[tmp_path],
    )

    assert result["ok"] is True
    assert calls[0][-4:] == ["wikipedia", "search", "-f", "json"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("expected_version", "installed_version"),
    [
        ("1.8.6", "1.8.7"),
        ("", "1.8.6"),
        ("1.8.6", ""),
    ],
)
async def test_generic_executor_rejects_unproven_or_mismatched_catalog_version(
    tmp_path: Path,
    expected_version: str,
    installed_version: str,
):
    calls: list[list[str]] = []

    def _unexpected_runner(argv, **kwargs):
        calls.append(list(argv))
        raise AssertionError("catalog drift must be rejected before dispatch")

    executor = OpenCLIExecutor(
        process_runner=_unexpected_runner,
        launcher_resolver=lambda: [
            "C:/trusted/node.exe",
            "C:/trusted/opencli/main.js",
        ],
        launcher_version_probe=lambda _argv: installed_version,
    )

    with pytest.raises(OpenCLIExecutionError) as caught:
        await executor.execute(
            _generic_contract(opencli_version=expected_version),
            arguments={"query": "safe"},
            workspace_roots=[tmp_path],
        )

    assert caught.value.code == "opencli_catalog_drift"
    assert caught.value.attempted is False
    assert caught.value.fallback_allowed is True
    assert calls == []


@pytest.mark.asyncio
async def test_generic_executor_rejects_non_public_or_browser_contract_before_start(
    tmp_path: Path,
):
    def _unexpected_runner(*args, **kwargs):
        raise AssertionError("unsafe generic contract must not start a process")

    executor = OpenCLIExecutor(process_runner=_unexpected_runner)
    for contract in (
        _generic_contract(semantic_effect="private_read"),
        _generic_contract(risk="high"),
        _generic_contract(auth="required"),
        _generic_contract(transport="browser_dom"),
        _generic_contract(browser=True),
        _generic_contract(access="write"),
        _generic_contract(confirmation="interactive_user"),
        _generic_contract(file_inputs=("path",)),
        _generic_contract(file_outputs=("path",)),
        _generic_contract(sensitive_output=("token",)),
        _generic_contract(execution_state="disabled"),
    ):
        with pytest.raises(OpenCLIExecutionError) as caught:
            await executor.execute(
                contract,
                arguments={"query": "safe"},
                workspace_roots=[tmp_path],
            )
        assert caught.value.attempted is False


@pytest.mark.asyncio
async def test_xiaohongshu_trusted_target_is_the_wheel_module_and_result_is_closed(
    tmp_path: Path,
):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")
    calls: list[list[str]] = []

    def _runner(argv, **kwargs):
        calls.append(list(argv))
        return subprocess.CompletedProcess(
            argv,
            1,
            stdout=json.dumps(
                {
                    "ok": False,
                    "mode": "draft",
                    "attempted": False,
                    "fallback_allowed": True,
                    "error": {
                        "code": "opencli_browser_unavailable",
                        "message": "Bridge unavailable",
                    },
                }
            ),
            stderr="",
        )

    result = await OpenCLIExecutor(
        process_runner=_runner,
        launcher_resolver=lambda: [
            "C:/trusted/node.exe",
            "C:/trusted/opencli/main.js",
        ],
        launcher_version_probe=lambda _argv: "1.8.6",
    ).execute(
        _xiaohongshu_contract(tmp_path),
        payload_path=str(payload),
        workspace_roots=[tmp_path],
    )

    assert result["ok"] is False
    assert result["attempted"] is True
    assert result["fallback_allowed"] is False
    assert calls == [
        [
            sys.executable,
            "-E",
            "-I",
            "-m",
            ("jiuwenswarm.agents.harness.common.opencli.executors.xiaohongshu_publish"),
            "--payload",
            str(payload),
            "--expected-opencli-version",
            "1.8.6",
        ]
    ]
    assert "resources" not in " ".join(calls[0])
    assert "skills" not in " ".join(calls[0])


@pytest.mark.asyncio
async def test_started_process_with_bad_envelope_fails_closed(tmp_path: Path):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")

    def _runner(argv, **kwargs):
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout="not-json",
            stderr="",
        )

    with pytest.raises(OpenCLIExecutionError) as caught:
        await OpenCLIExecutor(
            process_runner=_runner,
            launcher_resolver=lambda: [
                "C:/trusted/node.exe",
                "C:/trusted/opencli/main.js",
            ],
            launcher_version_probe=lambda _argv: "1.8.6",
        ).execute(
            _xiaohongshu_contract(tmp_path),
            payload_path=str(payload),
            workspace_roots=[tmp_path],
        )

    assert caught.value.code == "opencli_executor_output_invalid"
    assert caught.value.attempted is True
    assert caught.value.fallback_allowed is False


@pytest.mark.asyncio
async def test_started_process_rejects_non_strict_json_envelope(
    tmp_path: Path,
):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")

    def _runner(argv, **kwargs):
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout=(
                '{"ok":false,"ok":true,"mode":"draft",'
                '"attempted":true,"fallback_allowed":false,'
                '"result":NaN}'
            ),
            stderr="",
        )

    executor = OpenCLIExecutor(
        process_runner=_runner,
        launcher_resolver=lambda: [
            "C:/trusted/node.exe",
            "C:/trusted/opencli/main.js",
        ],
        launcher_version_probe=lambda _argv: "1.8.6",
    )
    with pytest.raises(OpenCLIExecutionError) as caught:
        await executor.execute(
            _xiaohongshu_contract(tmp_path),
            payload_path=str(payload),
            workspace_roots=[tmp_path],
        )

    assert caught.value.code == "opencli_executor_output_invalid"
    assert caught.value.attempted is True
    assert caught.value.fallback_allowed is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "envelope",
    [
        {"ok": True},
        {
            "ok": True,
            "mode": "draft",
            "attempted": "true",
            "fallback_allowed": False,
            "result": {},
        },
        {
            "ok": True,
            "mode": 1,
            "attempted": True,
            "fallback_allowed": False,
            "result": {},
        },
    ],
)
async def test_started_process_with_malformed_envelope_fails_closed(
    tmp_path: Path,
    envelope,
):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")

    def _runner(argv, **kwargs):
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout=json.dumps(envelope),
            stderr="",
        )

    executor = OpenCLIExecutor(
        process_runner=_runner,
        launcher_resolver=lambda: [
            "C:/trusted/node.exe",
            "C:/trusted/opencli/main.js",
        ],
        launcher_version_probe=lambda _argv: "1.8.6",
    )
    with pytest.raises(OpenCLIExecutionError) as caught:
        await executor.execute(
            _xiaohongshu_contract(tmp_path),
            payload_path=str(payload),
            workspace_roots=[tmp_path],
        )

    assert caught.value.code == "opencli_executor_output_invalid"
    assert caught.value.attempted is True
    assert caught.value.fallback_allowed is False


def test_wheel_xiaohongshu_runtime_uses_only_fixed_opencli_command(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    payload = tmp_path / "payload.json"
    payload.write_text(
        json.dumps(
            {
                "title": "safe draft",
                "content": "content",
                "images": ["C:/workspace/image.png"],
                "mode": "draft",
            }
        ),
        encoding="utf-8",
    )
    calls: list[tuple[list[str], dict[str, object]]] = []

    def _run(argv, **kwargs):
        calls.append((list(argv), dict(kwargs)))
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout='{"note_id":"draft-1"}',
            stderr="",
        )

    monkeypatch.setattr(
        wheel_publish,
        "resolve_opencli_launcher",
        lambda: ["C:/trusted/node.exe", "C:/trusted/opencli/main.js"],
    )
    monkeypatch.setattr(
        wheel_publish,
        "resolve_opencli_package_version",
        lambda _argv: "1.8.6",
    )
    monkeypatch.setattr(
        wheel_publish,
        "_detect_text_image_adapter_issue",
        lambda request, runner: None,
    )
    monkeypatch.setattr(
        wheel_publish,
        "probe_opencli_runtime",
        lambda **kwargs: SimpleNamespace(dispatch_allowed=True),
    )
    monkeypatch.setattr(wheel_publish.subprocess, "run", _run)

    assert (
        wheel_publish.main(
            [
                "--payload",
                str(payload),
                "--expected-opencli-version",
                "1.8.6",
            ]
        )
        == 0
    )

    emitted = json.loads(capsys.readouterr().out)
    assert emitted["ok"] is True
    assert emitted["attempted"] is True
    argv, options = calls[0]
    assert argv[:4] == [
        "C:/trusted/node.exe",
        "C:/trusted/opencli/main.js",
        "xiaohongshu",
        "publish",
    ]
    assert argv[-4:] == ["--draft", "true", "-f", "json"]
    assert options["shell"] is False
    assert "env" not in options


def test_wheel_xiaohongshu_runtime_rejects_catalog_drift_before_any_probe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    payload = tmp_path / "payload.json"
    payload.write_text(
        json.dumps(
            {
                "title": "safe draft",
                "content": "content",
                "images": ["C:/workspace/image.png"],
                "mode": "draft",
            }
        ),
        encoding="utf-8",
    )

    def _unexpected(*args, **kwargs):
        raise AssertionError("catalog drift must stop before runtime probes")

    monkeypatch.setattr(
        wheel_publish,
        "resolve_opencli_launcher",
        lambda: ["C:/trusted/node.exe", "C:/trusted/opencli/main.js"],
    )
    monkeypatch.setattr(
        wheel_publish,
        "resolve_opencli_package_version",
        lambda _argv: "1.8.7",
    )
    monkeypatch.setattr(
        wheel_publish,
        "_detect_text_image_adapter_issue",
        _unexpected,
    )
    monkeypatch.setattr(wheel_publish, "probe_opencli_runtime", _unexpected)
    monkeypatch.setattr(wheel_publish.subprocess, "run", _unexpected)

    assert (
        wheel_publish.main(
            [
                "--payload",
                str(payload),
                "--expected-opencli-version",
                "1.8.6",
            ]
        )
        != 0
    )

    emitted = json.loads(capsys.readouterr().out)
    assert emitted["error"]["code"] == "opencli_catalog_drift"
    assert emitted["attempted"] is False
    assert emitted["fallback_allowed"] is True


@pytest.mark.asyncio
async def test_xiaohongshu_outer_executor_rejects_catalog_drift_before_start(
    tmp_path: Path,
):
    payload = tmp_path / "payload.json"
    payload.write_text("{}", encoding="utf-8")

    def _unexpected_runner(*args, **kwargs):
        raise AssertionError("wheel runtime must not start on catalog drift")

    executor = OpenCLIExecutor(
        process_runner=_unexpected_runner,
        launcher_resolver=lambda: [
            "C:/trusted/node.exe",
            "C:/trusted/opencli/main.js",
        ],
        launcher_version_probe=lambda _argv: "1.8.7",
    )

    with pytest.raises(OpenCLIExecutionError) as caught:
        await executor.execute(
            _xiaohongshu_contract(tmp_path),
            payload_path=str(payload),
            workspace_roots=[tmp_path],
        )

    assert caught.value.code == "opencli_catalog_drift"
    assert caught.value.attempted is False
    assert caught.value.fallback_allowed is True


def test_wheel_xiaohongshu_runtime_has_no_binary_or_prefix_override_flags():
    parser = wheel_publish._build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "--payload",
                "payload.json",
                "--expected-opencli-version",
                "1.8.6",
                "--opencli-bin",
                "attacker-controlled",
            ]
        )
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "--payload",
                "payload.json",
                "--expected-opencli-version",
                "1.8.6",
                "--opencli-prefix-arg",
                "--profile=attacker-controlled",
            ]
        )


def test_opencli_package_module_entry_has_clean_stdout(
    tmp_path: Path,
):
    fake_package = tmp_path / "jiuwenswarm"
    fake_package.mkdir()
    (fake_package / "__init__.py").write_text(
        "raise RuntimeError('workspace package shadowed trusted runtime')\n",
        encoding="utf-8",
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-E",
            "-I",
            "-m",
            ("jiuwenswarm.agents.harness.common.opencli.executors.xiaohongshu_publish"),
            "--help",
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=tmp_path,
        shell=False,
        timeout=30,
    )

    assert completed.returncode == 0
    assert completed.stdout.startswith("usage: xiaohongshu_publish.py")
    assert "Registered connector pool" not in completed.stdout
    assert completed.stderr == ""


def test_opencli_package_lazy_exports_preserve_the_public_api():
    from jiuwenswarm.agents.harness.common import opencli
    from jiuwenswarm.agents.harness.common.opencli.contracts import (
        OPENCLI_WEB_SKILL_NAME,
    )
    from jiuwenswarm.agents.harness.common.opencli.disclosure import (
        DisclosureReceiptStore,
        get_opencli_disclosure_store,
    )
    from jiuwenswarm.agents.harness.common.opencli.rail import (
        OpenCLIDisclosureRail,
    )
    from jiuwenswarm.agents.harness.common.opencli.tool import (
        OPENCLI_EXECUTE_TOOL_NAME,
        OpenCLIExecuteTool,
    )

    assert opencli.OPENCLI_WEB_SKILL_NAME is OPENCLI_WEB_SKILL_NAME
    assert opencli.DisclosureReceiptStore is DisclosureReceiptStore
    assert opencli.get_opencli_disclosure_store is get_opencli_disclosure_store
    assert opencli.OpenCLIDisclosureRail is OpenCLIDisclosureRail
    assert opencli.OPENCLI_EXECUTE_TOOL_NAME is OPENCLI_EXECUTE_TOOL_NAME
    assert opencli.OpenCLIExecuteTool is OpenCLIExecuteTool


def test_windows_launcher_resolves_node_and_package_main_without_inputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    launcher_dir = tmp_path / "node portable"
    command_shim = launcher_dir / "opencli.cmd"
    node = launcher_dir / "node.exe"
    main_js = (
        launcher_dir
        / "node_modules"
        / "@jackwener"
        / "opencli"
        / "dist"
        / "src"
        / "main.js"
    )
    main_js.parent.mkdir(parents=True)
    command_shim.write_text("@echo off\n", encoding="utf-8")
    node.write_bytes(b"fixture")
    main_js.write_text("// fixture\n", encoding="utf-8")
    (main_js.parents[2] / "package.json").write_text(
        json.dumps(
            {
                "name": "@jackwener/opencli",
                "version": "1.8.6",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(launcher, "_IS_WINDOWS", True)
    monkeypatch.setattr(
        launcher.shutil,
        "which",
        lambda name: str(command_shim) if name in {"opencli", "opencli.cmd"} else None,
    )

    assert inspect.signature(launcher.resolve_opencli_launcher).parameters == {}
    resolved = launcher.resolve_opencli_launcher()
    assert resolved == [str(node), str(main_js)]
    assert launcher.resolve_opencli_package_version(resolved) == "1.8.6"


def test_posix_launcher_resolves_package_version_from_reviewed_main_js(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    main_js = (
        tmp_path
        / "lib"
        / "node_modules"
        / "@jackwener"
        / "opencli"
        / "dist"
        / "src"
        / "main.js"
    )
    main_js.parent.mkdir(parents=True)
    main_js.write_text("#!/usr/bin/env node\n", encoding="utf-8")
    (main_js.parents[2] / "package.json").write_text(
        json.dumps(
            {
                "name": "@jackwener/opencli",
                "version": "1.8.6",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(launcher, "_IS_WINDOWS", False)
    monkeypatch.setattr(
        launcher.shutil,
        "which",
        lambda name: str(main_js) if name == "opencli" else None,
    )

    resolved = launcher.resolve_opencli_launcher()

    assert resolved == [str(main_js)]
    assert launcher.resolve_opencli_package_version(resolved) == "1.8.6"


@pytest.mark.parametrize(
    "package",
    [
        {"name": "@jackwener/not-opencli", "version": "1.8.6"},
        {"name": "@jackwener/opencli", "version": ""},
        {"name": "@jackwener/opencli"},
        "not-an-object",
    ],
)
def test_launcher_rejects_package_metadata_that_cannot_prove_version(
    tmp_path: Path,
    package,
):
    main_js = (
        tmp_path
        / "node_modules"
        / "@jackwener"
        / "opencli"
        / "dist"
        / "src"
        / "main.js"
    )
    main_js.parent.mkdir(parents=True)
    main_js.write_text("// fixture\n", encoding="utf-8")
    (main_js.parents[2] / "package.json").write_text(
        json.dumps(package),
        encoding="utf-8",
    )

    with pytest.raises(launcher.OpenCLILauncherError) as caught:
        launcher.resolve_opencli_package_version([str(main_js)])

    assert caught.value.code == "opencli_catalog_drift"
