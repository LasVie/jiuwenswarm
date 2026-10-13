# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Decide whether a Browser Agent gets site commands, from its real binding.

The decision reads the Browser Agent's final Playwright MCP environment, not
the configuration: only a Browser Agent bound to the built-in Electron sidebar
(target resolver + session identity + Electron's own Node) qualifies. An
external Chrome binding strips these values, so it never qualifies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

ELECTRON_NODE_ENV = "JIUWENSWARM_ELECTRON_NODE"
_WORKER_PAGE_MODES = frozenset({"sidebar", "hidden"})


@dataclass(frozen=True)
class Binding:
    resolver: str
    token: str
    session_id: str
    member_id: str
    electron_node: str


@dataclass(frozen=True)
class OpenCLISettings:
    enabled: bool = False
    worker_page: str = "sidebar"
    enabled_sites: tuple[str, ...] | None = None


def read_settings(config: Mapping[str, Any] | None) -> OpenCLISettings:
    browser = (config or {}).get("browser") if isinstance(config, Mapping) else None
    raw = browser.get("opencli") if isinstance(browser, Mapping) else None
    if not isinstance(raw, Mapping):
        return OpenCLISettings()
    worker_page = str(raw.get("worker_page") or "sidebar").strip().lower()
    sites = raw.get("enabled_sites")
    return OpenCLISettings(
        enabled=raw.get("enabled") is True,
        worker_page=worker_page if worker_page in _WORKER_PAGE_MODES else "sidebar",
        enabled_sites=tuple(str(site) for site in sites) if isinstance(sites, (list, tuple)) else None,
    )


def resolve_binding(settings: Any) -> Binding | None:
    """Return the Electron binding of a Browser Agent's RuntimeSettings, or None."""
    params = getattr(getattr(settings, "mcp_cfg", None), "params", None) or {}
    env = params.get("env") if isinstance(params, Mapping) else None
    if not isinstance(env, Mapping):
        return None
    resolver = str(env.get("PLAYWRIGHT_MCP_TARGET_RESOLVER") or "").strip()
    token = str(env.get("PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN") or "").strip()
    session_id = str(env.get("PLAYWRIGHT_MCP_SESSION_ID") or "").strip()
    electron_node = str(env.get(ELECTRON_NODE_ENV) or "").strip()
    if not (resolver and token and session_id and electron_node):
        return None
    if not resolver.startswith("http://127.0.0.1"):
        return None
    return Binding(
        resolver=resolver,
        token=token,
        session_id=session_id,
        member_id=str(env.get("PLAYWRIGHT_MCP_MEMBER_ID") or "").strip(),
        electron_node=electron_node,
    )
