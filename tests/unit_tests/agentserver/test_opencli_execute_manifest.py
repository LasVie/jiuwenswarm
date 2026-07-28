from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

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


class RecordingExecutor(OpenCLIExecutor):
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self,
        contract,
        *,
        workspace_roots,
        payload_path=None,
        arguments=None,
    ) -> dict[str, Any]:
        self.calls.append(
            {
                "contract": contract,
                "workspace_roots": list(workspace_roots),
                "payload_path": payload_path,
                "arguments": arguments,
            }
        )
        return {
            "ok": True,
            "site": contract.site,
            "operation": contract.operation,
            "command": contract.command,
            "mode": "read",
            "attempted": True,
            "fallback_allowed": False,
            "result": {"items": []},
            "error": None,
            "exit_code": 0,
            "latency_ms": 1,
        }


def _install_skill(tmp_path: Path) -> tuple[Path, Path, Path]:
    skills_root = tmp_path / "skills"
    installed_skill = skills_root / "opencli-web"
    shutil.copytree(BUILTIN_SKILL, installed_skill)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return skills_root, installed_skill, workspace


async def _disclose(
    rail: OpenCLIDisclosureRail,
    installed_skill: Path,
    relative_path: str,
) -> None:
    await rail.after_tool_call(
        AgentCallbackContext(
            agent=None,
            inputs=ToolCallInputs(
                tool_name="skill_tool",
                tool_args={
                    "skill_name": "opencli-web",
                    "relative_file_path": relative_path,
                },
                tool_result=ToolOutput(
                    success=True,
                    data={
                        "skill_directory": str(installed_skill),
                        "skill_content": (installed_skill / relative_path).read_text(
                            encoding="utf-8"
                        ),
                    },
                ),
            ),
            session=None,
        )
    )


def _build(
    *,
    skills_root: Path,
    workspace: Path,
    executor: RecordingExecutor,
) -> tuple[OpenCLIDisclosureRail, OpenCLIExecuteTool]:
    store = DisclosureReceiptStore()
    scope = "single:manifest-test:main-agent"
    rail = OpenCLIDisclosureRail(
        scope=scope,
        skills_root=skills_root,
        receipt_store=store,
    )
    tool = OpenCLIExecuteTool(
        scope=scope,
        skills_root=skills_root,
        workspace_roots=[workspace],
        receipt_store=store,
        language="en",
        agent_id="main-agent",
        executor=executor,
    )
    return rail, tool


@pytest.mark.asyncio
async def test_site_terminal_disclosure_executes_manifest_bound_public_read(
    tmp_path: Path,
) -> None:
    skills_root, installed_skill, workspace = _install_skill(tmp_path)
    executor = RecordingExecutor()
    rail, tool = _build(
        skills_root=skills_root,
        workspace=workspace,
        executor=executor,
    )
    terminal = "sites/rest-countries/SKILL.md"

    missing = await tool.invoke(
        {
            "site": "rest-countries",
            "operation": "public-data",
            "command": "country",
            "arguments": {"name": "Singapore", "limit": 1},
        }
    )
    assert missing.success is False
    assert missing.data["error"]["code"] == "opencli_disclosure_required"

    await _disclose(rail, installed_skill, terminal)
    completed = await tool.invoke(
        {
            "site": "rest-countries",
            "operation": "public-data",
            "command": "country",
            "arguments": {"name": "Singapore", "limit": 1},
        }
    )

    assert completed.success is True
    assert len(executor.calls) == 1
    contract = executor.calls[0]["contract"]
    assert contract.manifest_backed is True
    assert contract.terminal_kind == "site"
    assert contract.terminal_relative_path == terminal
    assert executor.calls[0]["arguments"] == {
        "name": "Singapore",
        "limit": 1,
    }
    assert executor.calls[0]["payload_path"] is None


@pytest.mark.asyncio
async def test_operation_terminal_rejects_disabled_command_before_executor(
    tmp_path: Path,
) -> None:
    skills_root, installed_skill, workspace = _install_skill(tmp_path)
    executor = RecordingExecutor()
    rail, tool = _build(
        skills_root=skills_root,
        workspace=workspace,
        executor=executor,
    )
    await _disclose(
        rail,
        installed_skill,
        "sites/google/operations/web-search.md",
    )

    result = await tool.invoke(
        {
            "site": "google",
            "operation": "web-search",
            "command": "search",
            "arguments": {"keyword": "OpenJiuwen"},
        }
    )

    assert result.success is False
    assert result.data["error"]["code"] == "opencli_command_disabled"
    assert result.data["attempted"] is False
    assert result.data["fallback_allowed"] is True
    assert executor.calls == []


@pytest.mark.asyncio
async def test_enabled_state_change_invalidates_bound_receipt(
    tmp_path: Path,
) -> None:
    skills_root, installed_skill, workspace = _install_skill(tmp_path)
    executor = RecordingExecutor()
    rail, tool = _build(
        skills_root=skills_root,
        workspace=workspace,
        executor=executor,
    )
    terminal = "sites/rest-countries/SKILL.md"
    await _disclose(rail, installed_skill, terminal)
    (skills_root / "skills_state.json").write_text(
        json.dumps(
            {"skill_configs": {"opencli-web": {"enabled": True}}},
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    result = await tool.invoke(
        {
            "site": "rest-countries",
            "operation": "public-data",
            "command": "country",
            "arguments": {"name": "Singapore"},
        }
    )

    assert result.success is False
    assert result.data["error"]["code"] == "opencli_disclosure_state_changed"
    assert result.data["attempted"] is False
    assert result.data["fallback_allowed"] is False
    assert executor.calls == []


@pytest.mark.asyncio
async def test_explicit_disable_blocks_execution_even_with_stale_skill_copy(
    tmp_path: Path,
) -> None:
    skills_root, installed_skill, workspace = _install_skill(tmp_path)
    executor = RecordingExecutor()
    rail, tool = _build(
        skills_root=skills_root,
        workspace=workspace,
        executor=executor,
    )
    terminal = "sites/rest-countries/SKILL.md"
    await _disclose(rail, installed_skill, terminal)
    (skills_root / "skills_state.json").write_text(
        json.dumps(
            {"skill_configs": {"opencli-web": {"enabled": False}}},
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    result = await tool.invoke(
        {
            "site": "rest-countries",
            "operation": "public-data",
            "command": "country",
            "arguments": {"name": "Singapore"},
        }
    )

    assert result.success is False
    assert result.data["error"]["code"] == "opencli_skill_disabled"
    assert result.data["attempted"] is False
    assert result.data["fallback_allowed"] is False
    assert executor.calls == []


def test_failure_never_allows_fallback_after_attempt() -> None:
    result = OpenCLIExecuteTool._failure(
        "opencli_failed",
        "ambiguous result",
        site="example",
        operation="write",
        command="publish",
        attempted=True,
        fallback_allowed=True,
    )

    assert result.data["attempted"] is True
    assert result.data["fallback_allowed"] is False
