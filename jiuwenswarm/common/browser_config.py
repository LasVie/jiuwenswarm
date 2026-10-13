# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Browser settings shared by the local and AgentServer RPC paths."""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Mapping

from jiuwenswarm.common.config import resolve_env_vars


def resolve_browser_path(browser: Mapping[str, Any]) -> str:
    resolved = resolve_env_vars(dict(browser))
    chrome_path = resolved.get("chrome_path", "")
    if isinstance(chrome_path, str):
        return chrome_path.strip()
    if not isinstance(chrome_path, dict):
        return ""
    platform_key = {"win32": "windows", "cygwin": "windows", "darwin": "macos",
                    "linux": "linux", "linux2": "linux"}.get(sys.platform, "default")
    for key in (platform_key, "default"):
        value = chrome_path.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def browser_config_updates(params: Any) -> dict[str, Any]:
    """Validate a partial patch; omitted fields retain their current values."""
    if not isinstance(params, dict):
        raise ValueError("params must be object")
    updates: dict[str, Any] = {}
    if "chrome_path" in params:
        if not isinstance(params["chrome_path"], str):
            raise ValueError("chrome_path must be string")
        updates["chrome_path"] = params["chrome_path"].strip()
    if "headless" in params:
        # Retain the established browser RPC's fallback for legacy clients.
        updates["headless"] = params["headless"] if isinstance(params["headless"], bool) else True
    if "opencli" in params:
        raw = params["opencli"]
        if not isinstance(raw, dict):
            raise ValueError("opencli must be object")
        if set(raw) - {"enabled", "worker_page", "enabled_sites"}:
            raise ValueError("unsupported opencli setting")
        options: dict[str, Any] = {}
        if "enabled" in raw:
            if not isinstance(raw["enabled"], bool):
                raise ValueError("opencli.enabled must be boolean")
            options["enabled"] = raw["enabled"]
        if "worker_page" in raw:
            if raw["worker_page"] not in ("sidebar", "hidden"):
                raise ValueError("opencli.worker_page must be sidebar or hidden")
            options["worker_page"] = raw["worker_page"]
        if "enabled_sites" in raw:
            sites = raw["enabled_sites"]
            if sites is not None and (not isinstance(sites, list)
                                      or any(not isinstance(site, str) or not site.strip() for site in sites)):
                raise ValueError("opencli.enabled_sites must be null or a list of site names")
            options["enabled_sites"] = None if sites is None else list(dict.fromkeys(site.strip() for site in sites))
        if options:
            updates["opencli"] = options
    if not updates:
        raise ValueError("browser settings patch must contain at least one field")
    return updates


def merge_browser_config(config: Mapping[str, Any], updates: Mapping[str, Any]) -> dict[str, Any]:
    raw_browser = config.get("browser")
    browser = dict(raw_browser) if isinstance(raw_browser, Mapping) else {}
    for key, value in updates.items():
        if key == "opencli":
            previous = browser.get(key)
            browser[key] = {**(dict(previous) if isinstance(previous, Mapping) else {}), **value}
        else:
            browser[key] = value
    return {**config, "browser": browser}


def browser_runtime_changed(config: Mapping[str, Any], updates: Mapping[str, Any]) -> bool:
    before = config.get("browser")
    before = before if isinstance(before, Mapping) else {}
    after = merge_browser_config(config, updates)["browser"]
    return (resolve_browser_path(before), before.get("headless", True)) != (
        resolve_browser_path(after), after.get("headless", True)
    )


def _electron_node_info() -> tuple[str | None, str | None]:
    """Read authoritative launcher/discovery data without changing the environment."""
    from jiuwenswarm.agents.harness.common.electron_sideview import load_electron_browser_endpoints

    if os.getenv("JIUWENSWARM_BROWSER_FORCE_MANAGED", "").strip().lower() in {"1", "true", "yes", "on"}:
        return None, None
    if os.getenv("BROWSER_DRIVER", "").strip().lower() not in {"", "remote"}:
        return None, None
    try:
        env = json.loads(os.getenv("PLAYWRIGHT_MCP_ENV_JSON") or "{}")
    except ValueError:
        env = {}
    env = env if isinstance(env, dict) else {}
    resolver = os.getenv("PLAYWRIGHT_MCP_TARGET_RESOLVER") or env.get("PLAYWRIGHT_MCP_TARGET_RESOLVER")
    if resolver:
        if not str(resolver).startswith("http://127.0.0.1:") or not env.get("PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN"):
            return None, None
        return _node_info_from_env(env)
    endpoints = load_electron_browser_endpoints()
    env = endpoints.get("env_json") if endpoints else None
    if not isinstance(env, dict):
        return None, None
    return _node_info_from_env(env)


def _node_info_from_env(env: Mapping[str, Any]) -> tuple[str | None, str | None]:
    node = env.get("JIUWENSWARM_ELECTRON_NODE")
    version = env.get("JIUWENSWARM_ELECTRON_NODE_VERSION")
    return (
        node.strip() or None if isinstance(node, str) else None,
        version.strip() or None if isinstance(version, str) else None,
    )


def browser_config_payload(config: Mapping[str, Any]) -> dict[str, Any]:
    from jiuwenswarm.extensions.opencli import diagnose
    from jiuwenswarm.extensions.opencli.gate import read_settings

    browser = config.get("browser")
    browser = browser if isinstance(browser, Mapping) else {}
    chrome_path = resolve_browser_path(browser)
    options = read_settings(config)
    node, node_version = _electron_node_info() if options.enabled and not chrome_path else (None, None)
    return {
        "chrome_path": chrome_path,
        "headless": browser.get("headless") if isinstance(browser.get("headless"), bool) else True,
        "opencli": {"enabled": options.enabled, "worker_page": options.worker_page,
                    "enabled_sites": list(options.enabled_sites) if options.enabled_sites is not None else None},
        "opencli_status": diagnose(config, node, node_version=node_version),
    }
