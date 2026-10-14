# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""OpenCLI contribution at the Code adapter and Swarm member assembly points (M3)."""

from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from openjiuwen.core.foundation.tool import McpServerConfig
from openjiuwen.core.single_agent.schema.agent_card import AgentCard
from openjiuwen.harness.tools.browser_move.playwright_runtime.config import (
    BrowserInstanceConfig,
    BrowserRunGuardrails,
    RuntimeSettings,
)

import jiuwenswarm.common.utils as common_utils
from jiuwenswarm.agents.swarm import browser_runtime
from jiuwenswarm.agents.swarm.context import SwarmBuildContext
from jiuwenswarm.agents.swarm.providers import code_subagents
from jiuwenswarm.common.playwright_mcp_runtime import PlaywrightMcpLaunch
from jiuwenswarm.extensions.opencli.catalog import Catalog
from jiuwenswarm.extensions.opencli.sources import opencli as source_module
from jiuwenswarm.extensions.opencli.sources.opencli import OpenCLIRuntime
from jiuwenswarm.server.runtime.agent_adapter import interface_code
from jiuwenswarm.server.runtime.agent_adapter.interface_code import JiuwenSwarmCodeAdapter

RESOLVER = "http://127.0.0.1:43124"
ENABLED = {"browser": {"opencli": {"enabled": True}}}


@pytest.fixture(autouse=True)
def electron_environment(monkeypatch, tmp_path: Path):
    env = {key: value for key, value in os.environ.items() if not key.startswith((
        "BROWSER_", "PLAYWRIGHT_", "JIUWENSWARM_ELECTRON", "JIUWENSWARM_BROWSER_",
    ))}
    env.update(BROWSER_DRIVER="remote", PLAYWRIGHT_MCP_TARGET_RESOLVER=RESOLVER, JIUWENSWARM_ELECTRON="1",
               JIUWENSWARM_DATA_DIR=str(tmp_path))
    monkeypatch.setattr(os, "environ", env)
    monkeypatch.setattr(browser_runtime, "get_user_workspace_dir", lambda: tmp_path)
    monkeypatch.setattr(browser_runtime, "resolve_playwright_mcp_launch", lambda *, environ: (
        PlaywrightMcpLaunch("bundled", "node", ("/bundled/cli.js",), "0.0.78")
    ))
    catalog = Catalog.from_payload(
        {"commands": [{"site": "bilibili", "command": "hot", "needs_browser": True}]}, source="opencli",
    )
    runtime = OpenCLIRuntime(cli_path=tmp_path / "main.js", node_command="node", node_version="24.0.0",
                             version="1.8.8", catalog=catalog, home_dir=tmp_path, cache_dir=tmp_path)
    monkeypatch.setattr(source_module, "prepare_runtime", lambda node_command, **kw: runtime)
    monkeypatch.setattr(common_utils, "get_user_workspace_dir", lambda: tmp_path)


def _settings() -> RuntimeSettings:
    # The process-wide PLAYWRIGHT_MCP_ENV_JSON from Electron supplies the token and Electron Node.
    return RuntimeSettings(
        provider="OpenAI", api_key="synthetic-not-used", api_base="https://example.invalid/v1",
        model_name="synthetic-not-used", guardrails=BrowserRunGuardrails(),
        instance=BrowserInstanceConfig(key="original"),
        mcp_cfg=McpServerConfig(
            server_id="original", server_name="original", server_path="stdio://playwright", client_type="stdio",
            params={"command": "electron.exe", "args": ["target_mcp_wrapper.cjs"],
                    "env": {"PLAYWRIGHT_MCP_TARGET_RESOLVER": RESOLVER,
                            "PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN": "synthetic-token",
                            "JIUWENSWARM_ELECTRON_NODE": "/app/WorkSwarm"}},
        ),
    )


def _browser_spec(*args, **kwargs) -> SimpleNamespace:
    return SimpleNamespace(
        factory_kwargs={"settings": _settings()},
        tools=[],
        system_prompt="You are a browser agent.",
        language="en",
        workspace=None,
        agent_card=AgentCard(name="browser_agent", description="Browser subagent."),
    )


def _opencli_tools(spec) -> list:
    return [tool for tool in spec.tools or [] if tool.card.name.startswith("opencli_")]


def _member(config: dict, name: str):
    ctx = SwarmBuildContext(mode="code.team", role="teammate", member_name=name, session_id="team-1", config=config)
    ctx.extras["_parent_model"] = object()
    return code_subagents.build_swarm_browser_agent({}, ctx)


def test_swarm_members_get_their_own_worker_pages(monkeypatch) -> None:
    monkeypatch.setattr(code_subagents, "build_browser_agent_config", _browser_spec)
    alice, bob = _member(ENABLED, "alice"), _member(ENABLED, "bob")
    for spec in (alice, bob):
        assert [tool.card.name for tool in _opencli_tools(spec)] == ["opencli_describe", "opencli_run"]
        assert "bilibili" in spec.system_prompt and "bilibili" in spec.agent_card.description
    slots = [_opencli_tools(spec)[1]._context.slot for spec in (alice, bob)]
    assert [slot._client._binding.member_id for slot in slots] == ["alice", "bob"]
    # Separate members never share a page lock, hold or pending-write record.
    assert slots[0]._state is not slots[1]._state


@pytest.mark.parametrize("config", [
    {"browser": {"opencli": {"enabled": False}}},
    # The external Chrome fallback strips the sidebar binding, so it never qualifies.
    {"browser": {"chrome_path": "/chrome", "opencli": {"enabled": True}}},
])
def test_swarm_member_without_opencli(monkeypatch, config) -> None:
    monkeypatch.setattr(code_subagents, "build_browser_agent_config", _browser_spec)
    spec = _member(config, "alice")
    assert _opencli_tools(spec) == []
    assert spec.system_prompt == "You are a browser agent." and spec.agent_card.description == "Browser subagent."


def _code_browser_spec(monkeypatch, tmp_path: Path, config_base: dict):
    adapter = JiuwenSwarmCodeAdapter()
    adapter._workspace_dir = str(tmp_path)
    adapter._project_dir = str(tmp_path)
    adapter._coding_memory_rail = None
    adapter._sys_operation = MagicMock()
    adapter._parent_session_id = "code-session"
    monkeypatch.setattr(adapter, "_browser_runtime_enabled", lambda: True)
    monkeypatch.setattr(adapter, "_prepare_browser_runtime_security", lambda spec: None)
    monkeypatch.setattr(interface_code, "build_browser_agent_config", _browser_spec)
    subagents, _ = adapter._build_configured_subagents(
        MagicMock(), {"max_iterations": 20, "subagents": {"browser_agent": {"enabled": True}}}, config_base
    )
    return next(spec for spec in subagents if getattr(spec, "agent_card", None) and spec.agent_card.name == "browser_agent")


def test_code_agent_browser_gets_site_commands_when_enabled(monkeypatch, tmp_path: Path) -> None:
    spec = _code_browser_spec(monkeypatch, tmp_path, ENABLED)
    assert [tool.card.name for tool in _opencli_tools(spec)] == ["opencli_describe", "opencli_run"]
    assert "bilibili" in spec.agent_card.description
    assert spec.factory_kwargs["auto_create_workspace"] is False


def test_code_agent_browser_is_unchanged_when_disabled(monkeypatch, tmp_path: Path) -> None:
    spec = _code_browser_spec(monkeypatch, tmp_path, {"browser": {"opencli": {"enabled": False}}})
    assert _opencli_tools(spec) == []
    assert spec.system_prompt == "You are a browser agent." and spec.agent_card.description == "Browser subagent."
