from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
import threading
from pathlib import Path

import pytest
from openjiuwen.core.single_agent.rail.base import (
    AgentCallbackContext,
    ToolCallInputs,
)
from openjiuwen.harness.tools import ToolOutput

from jiuwenswarm.agents.harness.common.opencli import (
    DisclosureReceiptStore,
    OpenCLIDisclosureRail,
    OpenCLIExecuteTool,
)
from jiuwenswarm.agents.harness.common.opencli.contracts import (
    load_operation_contract,
)
from jiuwenswarm.agents.harness.common.opencli.executor import OpenCLIExecutor


REPO_ROOT = Path(__file__).resolve().parents[3]
BUILTIN_SKILL = (
    REPO_ROOT
    / "jiuwenswarm"
    / "resources"
    / "agent"
    / "workspace"
    / "skills"
    / "opencli-web"
)
OPERATION_PATH = "sites/xiaohongshu/operations/publishing.md"


def _install_skill(tmp_path: Path) -> tuple[Path, Path]:
    skills_root = tmp_path / "skills"
    installed_skill = skills_root / "opencli-web"
    shutil.copytree(BUILTIN_SKILL, installed_skill)
    return skills_root, installed_skill


async def _disclose(
    rail: OpenCLIDisclosureRail,
    installed_skill: Path,
    *,
    result_success: bool = True,
    skill_directory: Path | None = None,
) -> None:
    content = (installed_skill / OPERATION_PATH).read_text(encoding="utf-8")
    await rail.after_tool_call(
        AgentCallbackContext(
            agent=None,
            inputs=ToolCallInputs(
                tool_name="skill_tool",
                tool_args={
                    "skill_name": "opencli-web",
                    "relative_file_path": OPERATION_PATH,
                },
                tool_result=ToolOutput(
                    success=result_success,
                    data={
                        "skill_directory": str(
                            skill_directory or installed_skill
                        ),
                        "skill_content": content,
                    },
                ),
            ),
            session=None,
        )
    )


def _tool(
    *,
    scope: str,
    skills_root: Path,
    workspace: Path,
    store: DisclosureReceiptStore,
    process_runner,
) -> OpenCLIExecuteTool:
    return OpenCLIExecuteTool(
        scope=scope,
        skills_root=skills_root,
        workspace_roots=[workspace],
        receipt_store=store,
        language="en",
        agent_id="main-agent",
        executor=OpenCLIExecutor(process_runner=process_runner),
    )


def _inputs(payload_path: Path) -> dict[str, str]:
    return {
        "site": "xiaohongshu",
        "operation": "publishing",
        "command": "publish",
        "payload_path": str(payload_path),
    }


@pytest.mark.asyncio
async def test_opencli_execute_requires_exact_disclosure_and_consumes_it_once(
    tmp_path: Path,
) -> None:
    skills_root, installed_skill = _install_skill(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = workspace / "payload.json"
    payload_path.write_text('{"title":"draft"}', encoding="utf-8")
    calls: list[list[str]] = []

    def _runner(argv, **kwargs):
        calls.append(list(argv))
        assert kwargs["shell"] is False
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout=json.dumps(
                {
                    "ok": True,
                    "mode": "draft",
                    "attempted": True,
                    "fallback_allowed": False,
                    "result": {"note_id": "draft-1"},
                }
            ),
            stderr="",
        )

    store = DisclosureReceiptStore()
    scope = "single:session-1:main-agent"
    rail = OpenCLIDisclosureRail(
        scope=scope,
        skills_root=skills_root,
        receipt_store=store,
    )
    tool = _tool(
        scope=scope,
        skills_root=skills_root,
        workspace=workspace,
        store=store,
        process_runner=_runner,
    )

    missing = await tool.invoke(_inputs(payload_path))
    assert missing.success is False
    assert missing.data["error"]["code"] == "opencli_disclosure_required"
    assert calls == []

    await _disclose(rail, installed_skill)
    completed = await tool.invoke(_inputs(payload_path))

    assert completed.success is True
    assert completed.data["site"] == "xiaohongshu"
    assert completed.data["operation"] == "publishing"
    assert completed.data["command"] == "publish"
    assert completed.data["attempted"] is True
    assert len(calls) == 1
    assert calls[0][1] == "-E"
    assert calls[0][-2:] == ["--payload", str(payload_path)]
    assert Path(calls[0][2]).as_posix().endswith(
        "sites/xiaohongshu/scripts/publish.py"
    )

    replay = await tool.invoke(_inputs(payload_path))
    assert replay.success is False
    assert replay.data["error"]["code"] == "opencli_disclosure_required"
    assert len(calls) == 1


@pytest.mark.asyncio
async def test_disclosure_is_scope_bound_and_rejects_non_skill_results(
    tmp_path: Path,
) -> None:
    skills_root, installed_skill = _install_skill(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = workspace / "payload.json"
    payload_path.write_text("{}", encoding="utf-8")

    def _unexpected_runner(*args, **kwargs):
        raise AssertionError("executor must not run")

    store = DisclosureReceiptStore()
    main_rail = OpenCLIDisclosureRail(
        scope="main",
        skills_root=skills_root,
        receipt_store=store,
    )
    other_tool = _tool(
        scope="general-purpose",
        skills_root=skills_root,
        workspace=workspace,
        store=store,
        process_runner=_unexpected_runner,
    )

    await _disclose(main_rail, installed_skill, result_success=False)
    failed_read = await other_tool.invoke(_inputs(payload_path))
    assert failed_read.data["error"]["code"] == "opencli_disclosure_required"

    await _disclose(
        main_rail,
        installed_skill,
        skill_directory=tmp_path / "untrusted-skill-copy",
    )
    wrong_directory = await other_tool.invoke(_inputs(payload_path))
    assert wrong_directory.data["error"]["code"] == "opencli_disclosure_required"

    await _disclose(main_rail, installed_skill)
    wrong_scope = await other_tool.invoke(_inputs(payload_path))
    assert wrong_scope.data["error"]["code"] == "opencli_disclosure_required"


@pytest.mark.asyncio
async def test_disclosure_accepts_declared_member_skill_copy(
    tmp_path: Path,
) -> None:
    """A declared copied team view can grant the same hash-bound receipt."""
    skills_root, installed_skill = _install_skill(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = workspace / "payload.json"
    payload_path.write_text("{}", encoding="utf-8")
    member_skill_copy = tmp_path / "member" / "skills" / "opencli-web"
    shutil.copytree(installed_skill, member_skill_copy)
    calls: list[list[str]] = []

    def _runner(argv, **kwargs):
        calls.append(list(argv))
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout='{"ok":true,"attempted":true,"fallback_allowed":false}',
            stderr="",
        )

    store = DisclosureReceiptStore()
    rail = OpenCLIDisclosureRail(
        scope="team-leader",
        skills_root=skills_root,
        receipt_store=store,
        allowed_skill_directories=[member_skill_copy],
    )
    tool = _tool(
        scope="team-leader",
        skills_root=skills_root,
        workspace=workspace,
        store=store,
        process_runner=_runner,
    )

    await _disclose(
        rail,
        installed_skill,
        skill_directory=member_skill_copy,
    )
    result = await tool.invoke(_inputs(payload_path))

    assert result.success is True
    assert len(calls) == 1


@pytest.mark.asyncio
async def test_opencli_execute_rejects_changed_contract_and_outside_payload(
    tmp_path: Path,
) -> None:
    skills_root, installed_skill = _install_skill(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    inside_payload = workspace / "payload.json"
    inside_payload.write_text("{}", encoding="utf-8")
    outside_payload = tmp_path / "outside.json"
    outside_payload.write_text("{}", encoding="utf-8")
    calls: list[object] = []

    def _runner(*args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(
            args[0],
            0,
            stdout='{"ok":true,"attempted":true,"fallback_allowed":false}',
            stderr="",
        )

    store = DisclosureReceiptStore()
    scope = "main"
    rail = OpenCLIDisclosureRail(
        scope=scope,
        skills_root=skills_root,
        receipt_store=store,
    )
    tool = _tool(
        scope=scope,
        skills_root=skills_root,
        workspace=workspace,
        store=store,
        process_runner=_runner,
    )

    await _disclose(rail, installed_skill)
    outside = await tool.invoke(_inputs(outside_payload))
    assert outside.data["error"]["code"] == "opencli_payload_outside_workspace"
    assert calls == []

    operation_file = installed_skill / OPERATION_PATH
    operation_file.write_text(
        operation_file.read_text(encoding="utf-8") + "\n<!-- changed -->\n",
        encoding="utf-8",
    )
    changed = await tool.invoke(_inputs(inside_payload))
    assert changed.data["error"]["code"] == "opencli_disclosure_changed"
    assert calls == []


@pytest.mark.asyncio
async def test_opencli_execute_preserves_guarded_failure_classification(
    tmp_path: Path,
) -> None:
    skills_root, installed_skill = _install_skill(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = workspace / "payload.json"
    payload_path.write_text("{}", encoding="utf-8")

    def _runner(argv, **kwargs):
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
                        "message": "Browser bridge is disconnected",
                    },
                }
            ),
            stderr="",
        )

    store = DisclosureReceiptStore()
    scope = "main"
    rail = OpenCLIDisclosureRail(
        scope=scope,
        skills_root=skills_root,
        receipt_store=store,
    )
    tool = _tool(
        scope=scope,
        skills_root=skills_root,
        workspace=workspace,
        store=store,
        process_runner=_runner,
    )
    await _disclose(rail, installed_skill)

    result = await tool.invoke(_inputs(payload_path))

    assert result.success is False
    assert result.data["attempted"] is False
    assert result.data["fallback_allowed"] is True
    assert result.data["error"]["code"] == "opencli_browser_unavailable"


@pytest.mark.asyncio
async def test_executor_cancellation_does_not_orphan_guarded_process(
    tmp_path: Path,
) -> None:
    """A cancelled Agent waits for the bounded write process to terminate."""
    skills_root, _ = _install_skill(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    payload_path = workspace / "payload.json"
    payload_path.write_text("{}", encoding="utf-8")
    started = threading.Event()
    release = threading.Event()

    def _runner(argv, **kwargs):
        started.set()
        assert release.wait(timeout=2)
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout='{"ok":true,"attempted":true,"fallback_allowed":false}',
            stderr="",
        )

    contract = load_operation_contract(
        skills_root,
        "xiaohongshu",
        "publishing",
    ).command_contract("publish")
    executor = OpenCLIExecutor(process_runner=_runner)
    task = asyncio.create_task(
        executor.execute(
            contract,
            payload_path=str(payload_path),
            workspace_roots=[workspace],
        )
    )
    assert await asyncio.to_thread(started.wait, 1)

    task.cancel()
    await asyncio.sleep(0)
    assert task.done() is False

    release.set()
    with pytest.raises(asyncio.CancelledError):
        await task


def test_disclosure_receipt_expires() -> None:
    now = [10.0]
    store = DisclosureReceiptStore(
        ttl_seconds=5,
        clock=lambda: now[0],
    )
    store.grant(
        scope="main",
        site="xiaohongshu",
        operation="publishing",
        operation_sha256="abc",
    )
    now[0] = 16.0

    result = store.consume(
        scope="main",
        site="xiaohongshu",
        operation="publishing",
        operation_sha256="abc",
    )

    assert result.accepted is False
    assert result.code == "opencli_disclosure_expired"


@pytest.mark.asyncio
async def test_standalone_web_main_agent_tool_cards_include_opencli_execute(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cover the non-team Web adapter path that bypasses swarm providers."""
    from jiuwenswarm.server.runtime.agent_adapter import interface_deep

    skills_root, _ = _install_skill(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    adapter = interface_deep.JiuWenSwarmDeepAdapter()
    adapter.mark_as_session_scoped("standalone-opencli-test")
    adapter._project_dir = str(workspace)

    monkeypatch.setattr(interface_deep, "get_agent_skills_dir", lambda: skills_root)
    monkeypatch.setattr(interface_deep, "get_config", lambda: {})
    monkeypatch.setattr(interface_deep, "is_paid_search_enabled", lambda: False)
    monkeypatch.setattr(interface_deep, "is_skill_retrieval_enabled", lambda: False)
    monkeypatch.setattr(
        interface_deep.Runner.resource_mgr,
        "get_tool",
        lambda _tool_id: None,
    )
    monkeypatch.setattr(
        interface_deep.Runner.resource_mgr,
        "add_tool",
        lambda _tool: None,
    )
    monkeypatch.setattr(
        interface_deep.SymphonyToolkit,
        "get_tools",
        lambda self, config: [],
    )

    tool_cards = await adapter._get_tool_cards("standalone-opencli-agent")

    names = [card.name for card in tool_cards]
    assert names.count("opencli_execute") == 1
    assert adapter._opencli_execute_tool is not None
    assert adapter._opencli_execute_tool.card.parallel_safe is False
