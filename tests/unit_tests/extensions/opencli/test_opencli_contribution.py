# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Gate, zero exposure when off, and the Browser Agent contribution."""

from __future__ import annotations

import copy
from pathlib import Path
from types import SimpleNamespace

import pytest
from openjiuwen.core.single_agent.schema.agent_card import AgentCard

import jiuwenswarm.common.utils as common_utils
from jiuwenswarm.extensions.opencli import apply_opencli_contribution, diagnose
from jiuwenswarm.extensions.opencli.catalog import Catalog
from jiuwenswarm.extensions.opencli.gate import read_settings, resolve_binding
from jiuwenswarm.extensions.opencli.prompt import CARD_SITE_LIMIT, build_card_note, build_routing_prompt
from jiuwenswarm.extensions.opencli.sources import opencli as source_module
from jiuwenswarm.extensions.opencli.sources.opencli import OpenCLIRuntime, OpenCLIUnavailable

ELECTRON_ENV = {
    "PLAYWRIGHT_MCP_TARGET_RESOLVER": "http://127.0.0.1:4321",
    "PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN": "tk",
    "PLAYWRIGHT_MCP_SESSION_ID": "sess",
    "PLAYWRIGHT_MCP_MEMBER_ID": "",
    "JIUWENSWARM_ELECTRON_NODE": "C:/app/WorkSwarm.exe",
}
ENABLED = {"browser": {"opencli": {"enabled": True}}}


def _settings(env: dict | None):
    return SimpleNamespace(mcp_cfg=SimpleNamespace(params={"env": dict(env or {})}))


def _spec(env: dict | None) -> SimpleNamespace:
    return SimpleNamespace(
        factory_kwargs={"settings": _settings(env)},
        tools=["existing_tool"],
        system_prompt="You are a browser automation agent.",
        language="cn",
        workspace=None,
        agent_card=AgentCard(name="browser_agent", description="Dedicated browser subagent."),
    )


def test_read_settings_defaults_off() -> None:
    assert read_settings(None).enabled is False
    assert read_settings({"browser": {"opencli": {"enabled": "yes"}}}).enabled is False
    options = read_settings({"browser": {"opencli": {"enabled": True, "worker_page": "HIDDEN",
                                                     "enabled_sites": ["bilibili"]}}})
    assert (options.enabled, options.worker_page, options.enabled_sites) == (True, "hidden", ("bilibili",))
    assert read_settings({"browser": {"opencli": {"worker_page": "popup"}}}).worker_page == "sidebar"


def test_binding_requires_the_electron_sidebar() -> None:
    binding = resolve_binding(_settings(ELECTRON_ENV))
    assert binding is not None and binding.electron_node == "C:/app/WorkSwarm.exe"
    for missing in ("PLAYWRIGHT_MCP_TARGET_RESOLVER", "PLAYWRIGHT_MCP_SESSION_ID", "JIUWENSWARM_ELECTRON_NODE"):
        env = {**ELECTRON_ENV, missing: ""}
        assert resolve_binding(_settings(env)) is None
    # An external Chrome binding (env stripped) or a non-loopback resolver never qualifies.
    assert resolve_binding(_settings({})) is None
    assert resolve_binding(_settings({**ELECTRON_ENV, "PLAYWRIGHT_MCP_TARGET_RESOLVER": "http://evil:1"})) is None


@pytest.fixture
def no_probe(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("the runtime must not be probed")

    monkeypatch.setattr(source_module, "prepare_runtime", forbidden)


@pytest.mark.parametrize("config, env", [
    ({}, ELECTRON_ENV),
    ({"browser": {"opencli": {"enabled": False}}}, ELECTRON_ENV),
    (ENABLED, {}),  # external Chrome / no sidebar
])
def test_zero_exposure_when_off_or_unbound(no_probe, config, env) -> None:
    spec = _spec(env)
    before = copy.deepcopy((spec.tools, spec.system_prompt, spec.agent_card.description))
    assert apply_opencli_contribution(spec, config) is False
    assert (spec.tools, spec.system_prompt, spec.agent_card.description) == before


def test_unavailable_runtime_leaves_the_spec_unchanged(monkeypatch) -> None:
    def unavailable(node_command, **kwargs):
        raise OpenCLIUnavailable("electron_node_unavailable", "too old")

    monkeypatch.setattr(source_module, "prepare_runtime", unavailable)
    spec = _spec(ELECTRON_ENV)
    assert apply_opencli_contribution(spec, ENABLED) is False
    assert spec.tools == ["existing_tool"]


def _fake_runtime(tmp_path: Path) -> OpenCLIRuntime:
    catalog = Catalog.from_payload(
        {"commands": [{"site": "bilibili", "command": "search", "needs_browser": True},
                      {"site": "zhihu", "command": "hot", "needs_browser": True}]},
        source="opencli",
    )
    return OpenCLIRuntime(cli_path=tmp_path / "main.js", node_command="node", node_version="24.0.0",
                          version="1.8.8", catalog=catalog, home_dir=tmp_path, cache_dir=tmp_path)


def test_enabled_contribution_adds_two_tools_and_the_routing_prompt(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(source_module, "prepare_runtime", lambda node_command, **kw: _fake_runtime(tmp_path))
    monkeypatch.setattr(common_utils, "get_user_workspace_dir", lambda: tmp_path)
    spec = _spec(ELECTRON_ENV)
    assert apply_opencli_contribution(spec, {"browser": {"opencli": {"enabled": True, "enabled_sites": ["zhihu"]}}})
    assert spec.tools[0] == "existing_tool"
    assert [tool.card.name for tool in spec.tools[1:]] == ["opencli_describe", "opencli_run"]
    assert spec.system_prompt.startswith("You are a browser automation agent.")
    assert "zhihu" in spec.system_prompt and "bilibili" not in spec.system_prompt
    # The parent agent only sees the card, so it must name the enabled sites too.
    assert spec.agent_card.description.startswith("Dedicated browser subagent.")
    assert "OpenCLI" in spec.agent_card.description
    assert "zhihu" in spec.agent_card.description and "bilibili" not in spec.agent_card.description


def test_card_note_is_copied_not_mutated(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(source_module, "prepare_runtime", lambda node_command, **kw: _fake_runtime(tmp_path))
    monkeypatch.setattr(common_utils, "get_user_workspace_dir", lambda: tmp_path)
    spec = _spec(ELECTRON_ENV)
    shared_card = spec.agent_card
    assert apply_opencli_contribution(spec, ENABLED)
    assert shared_card.description == "Dedicated browser subagent."
    assert spec.agent_card is not shared_card and spec.agent_card.name == "browser_agent"


def test_routing_prompt_for_the_bundled_catalog_stays_small() -> None:
    resources = Path(source_module.__file__).resolve().parents[3] / "resources" / "runtime" / "opencli"
    catalog = Catalog.load(resources / "catalog.json", source="opencli")
    for language in ("cn", "en"):
        prompt = build_routing_prompt(catalog, language)
        assert "opencli_describe" in prompt
        # Describe each site once, and answer from command data instead of re-collecting it on the page.
        assert ("不要再逐个命令查询" if language == "cn" else "do not look up commands one by one") in prompt
        assert ("不要再打开页面重新采集或核对" if language == "cn" else "do not open the page to collect or check it again") in prompt
        # Names that do not reveal the site carry its domain; obvious names stay bare.
        assert "hackernews (news.ycombinator.com)" in prompt and "github-trending (github.com)" in prompt
        assert "bilibili (" not in prompt and "crates (" not in prompt
        assert ("已完成，继续" if language == "cn" else "Done, continue") in prompt
        # Roughly 1k tokens: the site list dominates and stays a single line.
        assert len(prompt) < 4000, len(prompt)


def test_card_note_for_the_bundled_catalog_stays_short() -> None:
    resources = Path(source_module.__file__).resolve().parents[3] / "resources" / "runtime" / "opencli"
    catalog = Catalog.load(resources / "catalog.json", source="opencli")
    assert len(catalog.sites()) > CARD_SITE_LIMIT
    for language in ("cn", "en"):
        note = build_card_note(catalog, language)
        assert catalog.sites()[0] in note
        assert catalog.sites()[-1] not in note
        assert ("more" if language == "en" else str(len(catalog.sites()))) in note
        assert len(note) < 700, len(note)


def test_diagnose_states(monkeypatch, tmp_path: Path) -> None:
    assert diagnose({}, "node") == {"state": "off"}
    assert diagnose(ENABLED, None)["state"] == "unsupported_browser_mode"
    monkeypatch.setattr(source_module, "inspect_runtime", lambda node_command, **kw: ("1.8.8", _fake_runtime(tmp_path).catalog))
    assert diagnose(ENABLED, "node", node_version="24.0.0") == {"state": "available", "version": "1.8.8", "node_version": "24.0.0",
                                         "site_count": 2}
