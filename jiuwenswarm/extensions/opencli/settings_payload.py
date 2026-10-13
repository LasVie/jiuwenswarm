# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""OpenCLI fields of the browser settings payload (path.get / path.set).

Kept free of ``jiuwenswarm.common.config`` so the Front config service can
build the same payload without importing the Runtime configuration stack.
"""

from __future__ import annotations

import json
import os
from typing import Any, Mapping


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


def opencli_settings_payload(config: Mapping[str, Any], chrome_path: str) -> dict[str, Any]:
    """Saved OpenCLI options plus the availability diagnostic shown on the settings page."""
    from jiuwenswarm.extensions.opencli import diagnose
    from jiuwenswarm.extensions.opencli.gate import read_settings

    options = read_settings(config)
    node, node_version = _electron_node_info() if options.enabled and not chrome_path else (None, None)
    return {
        "opencli": {"enabled": options.enabled, "worker_page": options.worker_page,
                    "enabled_sites": list(options.enabled_sites) if options.enabled_sites is not None else None},
        "opencli_status": diagnose(config, node, node_version=node_version),
    }
