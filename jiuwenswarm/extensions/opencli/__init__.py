# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Optional OpenCLI site commands for the Browser Agent.

Public surface:

* ``apply_opencli_contribution(spec, config)`` - called by the Browser Agent
  assembly points; adds two tools, a routing prompt and a card note telling the
  parent agent to delegate site tasks, or does nothing.
* ``diagnose(config, electron_node)`` - availability for the settings page.

When the feature is off or unavailable nothing is added, nothing is probed and
no environment is changed, so the agents' prompts and tool lists stay
byte-for-byte identical.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

logger = logging.getLogger(__name__)

__all__ = ["Contribution", "apply_opencli_contribution", "browser_agent_contribution", "diagnose"]


@dataclass(frozen=True)
class Contribution:
    tools: list[Any]
    prompt_text: str
    # Appended to the Browser Agent's card, which the parent agent reads when deciding to delegate.
    card_note: str = ""


def _work_dir(workspace: Any, fallback: Path) -> Path:
    root = getattr(workspace, "root_path", workspace)
    if root:
        path = Path(str(root)).expanduser()
        if path.is_dir():
            return path
    return fallback


def browser_agent_contribution(
    settings: Any,
    config: Mapping[str, Any] | None,
    *,
    language: str = "cn",
    workspace: Any = None,
) -> Contribution | None:
    """Return the tools and prompt for one Browser Agent, or None."""
    from jiuwenswarm.extensions.opencli.gate import read_settings, resolve_binding

    options = read_settings(config)
    if not options.enabled:
        return None
    binding = resolve_binding(settings)
    if binding is None:
        return None

    from jiuwenswarm.common.utils import get_user_workspace_dir
    from jiuwenswarm.extensions.opencli.pending import PendingStore
    from jiuwenswarm.extensions.opencli.prompt import build_card_note, build_routing_prompt
    from jiuwenswarm.extensions.opencli.sources.opencli import (
        OpenCLISource,
        OpenCLIUnavailable,
        prepare_runtime,
    )
    from jiuwenswarm.extensions.opencli.tools import OpenCLIToolContext, build_tools
    from jiuwenswarm.extensions.opencli.worker_page import HostBinding, get_slot

    try:
        runtime = prepare_runtime(binding.electron_node)
    except OpenCLIUnavailable as exc:
        logger.warning("[opencli] site commands unavailable (%s): %s", exc.state, exc.detail)
        return None
    catalog = runtime.catalog.filter_sites(options.enabled_sites)
    if not len(catalog):
        return None
    host = HostBinding(
        resolver=binding.resolver,
        token=binding.token,
        session_id=binding.session_id,
        member_id=binding.member_id,
        visibility=options.worker_page,
    )
    state_root = get_user_workspace_dir() / "runtime" / "opencli"
    context = OpenCLIToolContext(
        source=OpenCLISource(runtime),
        catalog=catalog,
        slot=get_slot(host),
        pending=PendingStore(state_root / "pending"),
        session_id=binding.session_id,
        member_id=binding.member_id,
        work_dir=_work_dir(workspace, runtime.home_dir),
        language="en" if language == "en" else "cn",
    )
    return Contribution(
        tools=build_tools(context),
        prompt_text=build_routing_prompt(catalog, context.language),
        card_note=build_card_note(catalog, context.language),
    )


def apply_opencli_contribution(spec: Any, config: Mapping[str, Any] | None) -> bool:
    """Add site commands to a Browser Agent ``SubAgentConfig`` when available.

    Must run after the spec's RuntimeSettings are final (sidebar binding
    applied), because the decision is based on the actual browser binding.
    """
    settings = (getattr(spec, "factory_kwargs", None) or {}).get("settings")
    if settings is None:
        return False
    try:
        contribution = browser_agent_contribution(
            settings,
            config,
            language=str(getattr(spec, "language", None) or "cn"),
            workspace=getattr(spec, "workspace", None),
        )
    except Exception:  # noqa: BLE001 - an optional capability must never break assembly
        logger.warning("[opencli] failed to build site commands; Browser Agent keeps its page tools", exc_info=True)
        return False
    if contribution is None:
        return False
    spec.tools = [*(spec.tools or []), *contribution.tools]
    spec.system_prompt = f"{spec.system_prompt or ''}\n\n{contribution.prompt_text}".strip()
    card = getattr(spec, "agent_card", None)
    if card is not None and contribution.card_note:
        # Copy rather than mutate: the card object may be shared with other specs.
        description = f"{card.description or ''} {contribution.card_note}".strip()
        spec.agent_card = card.model_copy(update={"description": description})
    return True


def diagnose(
    config: Mapping[str, Any] | None, electron_node: str | None, *, node_version: str | None = None,
) -> dict[str, Any]:
    """Settings availability from files and host data, without launching anything."""
    from jiuwenswarm.extensions.opencli.gate import read_settings

    options = read_settings(config)
    if not options.enabled:
        return {"state": "off"}
    if not electron_node:
        return {"state": "unsupported_browser_mode", "detail": "built-in browser is not active"}
    from jiuwenswarm.extensions.opencli.sources.opencli import OpenCLIUnavailable, inspect_runtime

    try:
        version, catalog = inspect_runtime(electron_node, node_version=node_version)
    except OpenCLIUnavailable as exc:
        return {"state": exc.state, "detail": exc.detail}
    catalog = catalog.filter_sites(options.enabled_sites)
    return {
        "state": "available" if catalog.sites() else "no_sites_enabled",
        "version": version,
        "node_version": node_version,
        "site_count": len(catalog.sites()),
    }
