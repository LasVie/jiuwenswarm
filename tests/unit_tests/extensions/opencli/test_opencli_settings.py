# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Settings patches, process-free diagnostics, and task configuration snapshots."""

from __future__ import annotations

import copy
import json
import os
import sys
import pytest
import yaml

from jiuwenswarm.common import browser_config, config as config_module
from jiuwenswarm.common.schema.agent import AgentRequest
from jiuwenswarm.common.schema.message import ReqMethod
from jiuwenswarm.extensions.opencli import diagnose
from jiuwenswarm.extensions.opencli.sources import opencli as source_module
from jiuwenswarm.extensions.opencli.worker_page import HostBinding, get_slot
from jiuwenswarm.server.runtime.gateway_adapter.config_adapter import ConfigAdapter

ENABLED = {"browser": {"opencli": {"enabled": True}}}


def test_nested_config_patch_preserves_sites_other_browser_fields_and_comments(monkeypatch, tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("browser:\n  chrome_path: /external/chrome\n  headless: false\n"
                    "  opencli:\n    enabled: false  # user preference\n    worker_page: sidebar\n"
                    "    enabled_sites: [bilibili]\nother: retained\n", encoding="utf-8")
    monkeypatch.setattr(config_module, "CONFIG_YAML_PATH", path)
    config_module.update_browser_in_config({"opencli": {"enabled": True}})
    config_module.update_browser_in_config({"opencli": {"worker_page": "hidden"}})
    saved = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert saved == {"browser": {"chrome_path": "/external/chrome", "headless": False,
                                 "opencli": {"enabled": True, "worker_page": "hidden", "enabled_sites": ["bilibili"]}},
                     "other": "retained"}
    assert "# user preference" in path.read_text(encoding="utf-8")


@pytest.mark.parametrize("params", [None, {}, {"opencli": None}, {"opencli": {"enabled": "true"}},
    {"opencli": {"worker_page": "popup"}}, {"opencli": {"enabled_sites": "bilibili"}},
    {"opencli": {"enabled_sites": [False]}}, {"opencli": {"enabled_sites": [""]}},
    {"opencli": {"unexpected": True}}])
def test_malformed_settings_are_rejected(params):
    with pytest.raises(ValueError):
        browser_config.browser_config_updates(params)


def test_partial_patches_only_restart_for_browser_launch_changes():
    config = {"browser": {"chrome_path": "", "headless": True, "opencli": {"enabled": False}}}
    assert not browser_config.browser_runtime_changed(config, {"opencli": {"enabled": True, "worker_page": "hidden"}})
    assert not browser_config.browser_runtime_changed(config, {"chrome_path": "", "headless": True})
    assert browser_config.browser_runtime_changed(config, {"chrome_path": "/chrome"})
    assert browser_config.browser_runtime_changed(config, {"headless": False})


def test_disabled_settings_do_not_read_discovery_or_runtime(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("disabled capability must not be inspected")
    monkeypatch.setattr(browser_config, "_electron_node_info", forbidden)
    monkeypatch.setattr(source_module, "inspect_runtime", forbidden)
    assert browser_config.browser_config_payload({})["opencli_status"] == {"state": "off"}


def test_external_browser_does_not_inspect_the_electron_runtime(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("external browser must not use Electron")
    monkeypatch.setattr(browser_config, "_electron_node_info", forbidden)
    monkeypatch.setattr(source_module, "inspect_runtime", forbidden)
    config = {"browser": {"chrome_path": {"default": "/chrome"}, "opencli": {"enabled": True}}}
    assert browser_config.browser_config_payload(config)["opencli_status"]["state"] == "unsupported_browser_mode"


@pytest.mark.parametrize("node, version, expected", [
    (42, "24.19.0", "unsupported_browser_mode"),
    (sys.executable, [24, 19, 0], "available"),
    (sys.executable, "18.0.0", "electron_node_unavailable"),
])
def test_host_data_is_read_without_mutation_and_malformed_values_do_not_break_settings(
    monkeypatch, node, version, expected,
):
    monkeypatch.delenv("JIUWENSWARM_BROWSER_FORCE_MANAGED", raising=False)
    monkeypatch.delenv("PLAYWRIGHT_MCP_TARGET_RESOLVER", raising=False)
    monkeypatch.setenv("BROWSER_DRIVER", "remote")
    monkeypatch.setenv("PLAYWRIGHT_MCP_ENV_JSON", json.dumps({
        "PLAYWRIGHT_MCP_TARGET_RESOLVER": "http://127.0.0.1:19826",
        "PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN": "fixture-token",
        "JIUWENSWARM_ELECTRON_NODE": node,
        "JIUWENSWARM_ELECTRON_NODE_VERSION": version,
    }))
    before = dict(os.environ)
    assert browser_config.browser_config_payload(ENABLED)["opencli_status"]["state"] == expected
    assert dict(os.environ) == before


def test_diagnostic_reads_files_without_spawning_extracting_or_changing_environment(monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        raise AssertionError("diagnostic must not prepare or execute the runtime")
    monkeypatch.setattr(source_module, "prepare_runtime", forbidden)
    monkeypatch.setattr(source_module, "_probe_node", forbidden)
    monkeypatch.setattr(source_module, "materialize_bundled_runtime", forbidden)
    before = dict(os.environ)
    existing_files = set(tmp_path.iterdir())
    result = diagnose(ENABLED, sys.executable, node_version="24.19.0")
    assert result["state"] == "available" and result["site_count"] > 100
    assert result["version"] == "1.8.8"
    assert dict(os.environ) == before
    assert set(tmp_path.iterdir()) == existing_files
    assert diagnose(ENABLED, sys.executable, node_version="18.0.0")["state"] == "electron_node_unavailable"
    assert diagnose(ENABLED, str(tmp_path / "missing.exe"))["state"] == "electron_node_unavailable"
    monkeypatch.setattr(source_module, "_RESOURCE_DIR", tmp_path)
    assert diagnose(ENABLED, sys.executable)["state"] == "runtime_missing"


def test_diagnostic_rejects_tampered_catalog_and_respects_site_restriction(monkeypatch, tmp_path):
    restricted = {"browser": {"opencli": {"enabled": True, "enabled_sites": ["bilibili"]}}}
    assert diagnose(restricted, sys.executable)["site_count"] == 1
    assert diagnose({"browser": {"opencli": {"enabled": True, "enabled_sites": []}}}, sys.executable)["state"] == "no_sites_enabled"
    resources = source_module._RESOURCE_DIR
    manifest = json.loads((resources / "manifest.json").read_text(encoding="utf-8"))
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (tmp_path / manifest["archive"]).write_bytes((resources / manifest["archive"]).read_bytes())
    (tmp_path / manifest["catalog"]).write_text('{"commands": []}', encoding="utf-8")
    monkeypatch.setattr(source_module, "_RESOURCE_DIR", tmp_path)
    assert diagnose(ENABLED, sys.executable)["state"] == "runtime_missing"


async def test_agentserver_patch_keeps_the_old_snapshot_and_does_not_restart(monkeypatch):
    current = {"browser": {"chrome_path": "", "headless": True,
                           "opencli": {"enabled": False, "worker_page": "sidebar", "enabled_sites": ["bilibili"]}}}
    old_snapshot = copy.deepcopy(current)
    monkeypatch.setattr(config_module, "get_config", lambda: current)
    def save(updates):
        current.update(browser_config.merge_browser_config(current, updates))
    monkeypatch.setattr(config_module, "update_browser_in_config", save)
    monkeypatch.setattr(browser_config, "_electron_node_info", lambda: (sys.executable, "24.19.0"))
    adapter = ConfigAdapter()
    response = await adapter.handle(AgentRequest(
        request_id="settings-patch", channel_id="web", req_method=ReqMethod.PATH_SET,
        params={"opencli": {"enabled": True, "worker_page": "hidden"}},
    ))
    assert response.ok and response.metadata["config_changed"]
    assert response.metadata["browser_runtime_restart"] is False
    assert response.payload["opencli"] == {"enabled": True, "worker_page": "hidden", "enabled_sites": ["bilibili"]}
    assert response.payload["opencli_status"]["site_count"] == 1
    assert old_snapshot["browser"]["opencli"]["enabled"] is False
    fetched = await adapter.handle(AgentRequest(request_id="settings-read", channel_id="web", req_method=ReqMethod.PATH_GET))
    assert fetched.payload == response.payload


async def test_new_task_uses_new_visibility_but_shares_the_same_page_lock(monkeypatch):
    from jiuwenswarm.extensions.opencli import worker_page
    monkeypatch.setattr(worker_page, "_SLOTS", {})
    bindings = []
    class Client:
        def __init__(self, binding):
            self.binding = binding
        async def acquire(self, lease):
            bindings.append(self.binding.visibility)
            return "ws://page"
        async def release(self, lease):
            pass
    monkeypatch.setattr(worker_page, "HostClient", Client)
    binding = HostBinding(resolver="http://127.0.0.1:9999", token="test", session_id="s")
    from dataclasses import replace
    import asyncio
    old = get_slot(binding)
    new = get_slot(replace(binding, visibility="hidden"))
    async def next_task():
        async with new.use():
            assert bindings == ["sidebar", "hidden"]
    async with old.use():
        task = asyncio.create_task(next_task())
        await asyncio.sleep(0)
        assert not task.done() and bindings == ["sidebar"]
    await task
    async with old.use():
        assert bindings[-1] == "sidebar"
