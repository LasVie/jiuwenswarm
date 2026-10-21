# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Claude Code 插件加载单元测试."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import jiuwenswarm.common.claude_plugins as plugins_mod
from jiuwenswarm.common.claude_plugins import claude_plugin_skill_dirs, discover_claude_plugins
from jiuwenswarm.server.runtime.agent_adapter.code_agent_rail import AgentTool
from jiuwenswarm.server.runtime.agent_config_service import AgentConfigService, UpdateAgentParams

_SIMPLIFIER_MD = """---
name: code-simplifier
description: Simplifies and refines code for clarity
model: opus
tools: Read, Edit, Grep
---

You are an expert code simplification specialist.
"""


def _make_plugin(root: Path, name: str, *, manifest: bool = True) -> Path:
    plugin_dir = root / name
    (plugin_dir / "agents").mkdir(parents=True)
    (plugin_dir / "agents" / f"{name}.md").write_text(_SIMPLIFIER_MD.replace("code-simplifier", name), encoding="utf-8")
    if manifest:
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": name, "version": "1.0.0"}), encoding="utf-8"
        )
    return plugin_dir


@pytest.fixture
def home(tmp_path, monkeypatch):
    user_home = tmp_path / "home"
    user_home.mkdir()
    monkeypatch.setattr(plugins_mod, "get_user_workspace_dir", lambda: user_home)
    return user_home


@pytest.fixture
def workspace(tmp_path):
    ws = tmp_path / "ws"
    ws.mkdir()
    return ws


def test_discover_user_and_project_plugins(home, workspace):
    _make_plugin(home / "plugins", "code-simplifier")
    _make_plugin(workspace / ".jiuwenswarm" / "plugins", "other", manifest=False)

    names = {p.name for p in discover_claude_plugins(workspace, config_base={})}

    assert names == {"code-simplifier", "other"}


def test_project_plugin_overrides_user_plugin(home, workspace):
    _make_plugin(home / "plugins", "code-simplifier")
    project_dir = _make_plugin(workspace / ".jiuwenswarm" / "plugins", "code-simplifier")

    (plugin,) = discover_claude_plugins(workspace, config_base={})

    assert plugin.root == project_dir


def test_disabled_plugin_is_skipped(home, workspace):
    _make_plugin(home / "plugins", "code-simplifier")
    config = {"claude_plugins": {"code-simplifier": {"enabled": False}}}

    assert discover_claude_plugins(workspace, config_base=config) == []


def test_dir_without_manifest_or_content_is_ignored(home, workspace):
    (home / "plugins" / "empty").mkdir(parents=True)

    assert discover_claude_plugins(workspace, config_base={}) == []


def test_skill_dirs(home, workspace):
    plugin_dir = _make_plugin(home / "plugins", "frontend-design")
    (plugin_dir / "skills" / "frontend-design").mkdir(parents=True)
    (plugin_dir / "skills" / "frontend-design" / "SKILL.md").write_text("---\nname: frontend-design\n---\n")

    assert claude_plugin_skill_dirs(workspace, config_base={}) == [str(plugin_dir / "skills")]


def test_plugin_agent_listed_namespaced(home, workspace):
    _make_plugin(home / "plugins", "code-simplifier")

    agents = {a.name: a for a in AgentConfigService(workspace).list_agents()}
    agent = agents["code-simplifier:code-simplifier"]

    assert agent.source == "plugin"
    assert agent.enabled is True
    assert agent.model is None  # Claude 模型别名按 inherit 处理
    assert agent.tools == ["Read", "Edit", "Grep"]
    assert agent.prompt.startswith("You are an expert code simplification specialist.")


def test_plugin_agent_cannot_be_updated(home, workspace):
    _make_plugin(home / "plugins", "code-simplifier")
    service = AgentConfigService(workspace)

    with pytest.raises(ValueError):
        service.update_agent("code-simplifier:code-simplifier", UpdateAgentParams(description="x"))
    with pytest.raises(ValueError):
        service.delete_agent("code-simplifier:code-simplifier")


def test_sub_session_id_is_path_safe():
    sid = AgentTool._build_sub_session_id(None, "parent", "code-simplifier:code-simplifier")

    assert ":" not in sid
    assert sid.startswith("parent_custom_code-simplifier_code-simplifier_")
