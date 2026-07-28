from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import urllib.error
from pathlib import Path
from types import SimpleNamespace

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = (
    REPO_ROOT
    / "jiuwenswarm"
    / "resources"
    / "agent"
    / "workspace"
    / "skills"
    / "opencli-web"
)
RUNTIME_SCRIPT = SKILL_ROOT / "scripts" / "opencli_runtime.py"
PUBLISH_WRAPPER = SKILL_ROOT / "sites" / "xiaohongshu" / "scripts" / "publish.py"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def _write_payload(tmp_path: Path, *, mode: str = "draft") -> Path:
    payload = {
        "title": "Runtime test",
        "content": "OpenCLI runtime classification",
        "card_text": "runtime card",
        "mode": mode,
    }
    if mode == "publish":
        payload["confirmation"] = {
            "action": "social_post_confirm",
            "id": "runtime-confirmation",
        }
    path = tmp_path / "payload.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_runtime_probe_checks_the_selected_profile_without_starting_daemon(
    monkeypatch,
):
    runtime = _load_module("_opencli_runtime_ready_test", RUNTIME_SCRIPT)
    observed: dict[str, object] = {}

    def _status(request_url: str, timeout_seconds: float):
        observed["url"] = request_url
        observed["timeout"] = timeout_seconds
        return {"ok": True, "extensionConnected": True}

    monkeypatch.setattr(runtime, "_request_status", _status)

    probe = runtime.probe_opencli_runtime(profile="work profile")

    assert probe.state == "ready"
    assert probe.dispatch_allowed is True
    assert probe.daemon_running is True
    assert probe.extension_connected is True
    assert "contextId=work+profile" in observed["url"]


def test_runtime_probe_leaves_daemon_autostart_to_the_real_opencli_command(
    monkeypatch,
):
    runtime = _load_module("_opencli_runtime_stopped_test", RUNTIME_SCRIPT)

    def _unreachable(*args, **kwargs):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(runtime, "_request_status", _unreachable)

    probe = runtime.probe_opencli_runtime()

    assert probe.state == "daemon_not_running"
    assert probe.dispatch_allowed is True
    assert probe.daemon_running is False
    assert probe.error_code is None


@pytest.mark.parametrize(
    ("status", "expected_state"),
    [
        (
            {"ok": True, "extensionConnected": False},
            "extension_not_connected",
        ),
        (
            {
                "ok": True,
                "extensionConnected": False,
                "profileRequired": True,
            },
            "profile_required",
        ),
        (
            {
                "ok": True,
                "extensionConnected": False,
                "profileDisconnected": True,
            },
            "profile_disconnected",
        ),
    ],
)
def test_runtime_probe_blocks_a_known_unusable_browser_route(
    monkeypatch,
    status,
    expected_state,
):
    runtime = _load_module(
        f"_opencli_runtime_{expected_state}_test",
        RUNTIME_SCRIPT,
    )
    monkeypatch.setattr(
        runtime,
        "_request_status",
        lambda request_url, timeout_seconds: status,
    )

    probe = runtime.probe_opencli_runtime()

    assert probe.state == expected_state
    assert probe.dispatch_allowed is False
    assert probe.daemon_running is True
    assert probe.extension_connected is False
    assert probe.error_code == "opencli_browser_unavailable"


@pytest.mark.parametrize(
    ("stdout", "stderr"),
    [
        (
            json.dumps(
                {
                    "ok": False,
                    "error": {
                        "code": "BROWSER_CONNECT",
                        "message": "not connected",
                    },
                }
            ),
            "",
        ),
        (
            "",
            "ok: false\nerror:\n  code: BROWSER_CONNECT\n"
            "  message: Browser Bridge extension is not connected.\n",
        ),
    ],
)
def test_runtime_classifies_typed_browser_connect_as_predispatch(
    stdout,
    stderr,
):
    runtime = _load_module("_opencli_runtime_error_test", RUNTIME_SCRIPT)

    assert runtime.opencli_error_code(stdout, stderr) == "BROWSER_CONNECT"
    assert runtime.is_browser_connect_failure(stdout, stderr) is True


@pytest.mark.parametrize(
    ("mode", "fallback_allowed"),
    [("draft", True), ("publish", False)],
)
def test_publish_wrapper_blocks_reported_runtime_failure_before_dispatch(
    tmp_path,
    monkeypatch,
    capsys,
    mode,
    fallback_allowed,
):
    wrapper = _load_module(
        f"_opencli_publish_preflight_{mode}_test",
        PUBLISH_WRAPPER,
    )
    payload_path = _write_payload(tmp_path, mode=mode)
    confirmation_dir = tmp_path / "confirmations"
    subprocess_called = False

    def _unexpected_subprocess(*args, **kwargs):
        nonlocal subprocess_called
        subprocess_called = True
        raise AssertionError("runtime failure must block adapter dispatch")

    probe = SimpleNamespace(
        state="extension_not_connected",
        dispatch_allowed=False,
        daemon_running=True,
        extension_connected=False,
        error_code="opencli_browser_unavailable",
        message="The OpenCLI Browser Bridge extension is not connected",
        detail="daemon /status reports extensionConnected=false",
        public_result=lambda: {
            "state": "extension_not_connected",
            "daemon_running": True,
            "extension_connected": False,
        },
    )
    monkeypatch.setattr(
        wrapper, "_resolve_opencli_argv", lambda executable: ["opencli"]
    )
    monkeypatch.setattr(
        wrapper,
        "_detect_text_image_adapter_issue",
        lambda request, runner: None,
    )
    monkeypatch.setattr(wrapper, "probe_opencli_runtime", lambda **kwargs: probe)
    monkeypatch.setattr(wrapper.subprocess, "run", _unexpected_subprocess)

    exit_code = wrapper.main(
        [
            "--payload",
            str(payload_path),
            "--confirmation-dir",
            str(confirmation_dir),
        ]
    )
    result = json.loads(capsys.readouterr().out)

    assert exit_code != 0
    assert subprocess_called is False
    assert result["error"]["code"] == "opencli_browser_unavailable"
    assert result["attempted"] is False
    assert result["fallback_allowed"] is fallback_allowed
    assert result["result"]["runtime"]["state"] == "extension_not_connected"
    assert not confirmation_dir.exists()


def test_publish_wrapper_reclassifies_browser_connect_after_daemon_autostart(
    tmp_path,
    monkeypatch,
    capsys,
):
    wrapper = _load_module(
        "_opencli_publish_browser_connect_test",
        PUBLISH_WRAPPER,
    )
    payload_path = _write_payload(tmp_path)
    runtime = SimpleNamespace(
        state="daemon_not_running",
        dispatch_allowed=True,
        daemon_running=False,
        extension_connected=None,
        error_code=None,
        message="",
        detail="",
    )
    child_error = (
        "ok: false\n"
        "error:\n"
        "  code: BROWSER_CONNECT\n"
        "  message: Browser Bridge extension is not connected.\n"
        "  exitCode: 69\n"
    )
    monkeypatch.setattr(
        wrapper, "_resolve_opencli_argv", lambda executable: ["opencli"]
    )
    monkeypatch.setattr(
        wrapper,
        "_detect_text_image_adapter_issue",
        lambda request, runner: None,
    )
    monkeypatch.setattr(wrapper, "probe_opencli_runtime", lambda **kwargs: runtime)
    monkeypatch.setattr(
        wrapper.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0],
            returncode=69,
            stdout="",
            stderr=child_error,
        ),
    )

    exit_code = wrapper.main(["--payload", str(payload_path)])
    result = json.loads(capsys.readouterr().out)

    assert exit_code == 69
    assert result["error"]["code"] == "opencli_browser_unavailable"
    assert "BROWSER_CONNECT" in result["error"]["detail"]
    assert result["attempted"] is False
    assert result["fallback_allowed"] is True
