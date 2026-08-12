# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""JiuwenSwarm's OpenCLI-first Browser/Web Agent assembly."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from openjiuwen.core.foundation.llm.model import Model
from openjiuwen.harness.rails import SkillUseRail
from openjiuwen.harness.schema.config import SubAgentConfig
from openjiuwen.harness.subagents.browser_agent import (
    build_browser_agent_config as _build_browser_agent_config,
)

from jiuwenswarm.agents.harness.common.rails.web_tool_routing_rail import (
    WebToolRoutingRail,
)
from jiuwenswarm.common.utils import get_agent_skills_dir


OPENCLI_WEB_SKILL_NAME = "opencli-web"


def build_web_agent_routing_rails(
    *,
    skills_dir: str | Path | None = None,
    disabled_skills: Iterable[str] | None = None,
) -> list[Any]:
    """Build the OpenCLI capability owned exclusively by Browser/Web Agent.

    When the installed skill is missing or execution-disabled, the Browser Agent
    receives no OpenCLI rails and remains a normal local-Playwright agent.
    """
    resolved_skills_dir = Path(skills_dir or get_agent_skills_dir())
    disabled = {str(name) for name in (disabled_skills or [])}
    skill_path = resolved_skills_dir / OPENCLI_WEB_SKILL_NAME / "SKILL.md"
    if OPENCLI_WEB_SKILL_NAME in disabled or not skill_path.is_file():
        return []

    return [
        SkillUseRail(
            skills_dir=str(resolved_skills_dir),
            skill_mode=SkillUseRail.SKILL_MODE_ALL,
            include_tools=True,
            enabled_skills=[OPENCLI_WEB_SKILL_NAME],
            disabled_skills=disabled,
        ),
        WebToolRoutingRail(),
    ]


def build_web_agent_config(
    model: Model,
    *,
    skills_dir: str | Path | None = None,
    disabled_skills: Iterable[str] | None = None,
    rails: list[Any] | None = None,
    **kwargs: Any,
) -> SubAgentConfig:
    """Build Browser Agent with OpenCLI-first routing and Playwright fallback."""
    routing_rails = build_web_agent_routing_rails(
        skills_dir=skills_dir,
        disabled_skills=disabled_skills,
    )
    final_rails = [*(rails or []), *routing_rails]
    return _build_browser_agent_config(
        model,
        rails=final_rails or None,
        **kwargs,
    )


def refresh_web_agent_routing_rails(
    config: SubAgentConfig,
    *,
    skills_dir: str | Path | None = None,
    disabled_skills: Iterable[str] | None = None,
) -> None:
    """Synchronize OpenCLI rails on an already-registered Browser Agent spec.

    Skill uninstall uses a lightweight refresh instead of rebuilding the parent
    agent. Replacing only the two rails owned here keeps later Browser Agent
    invocations from retaining a removed OpenCLI skill while preserving any
    unrelated caller-provided rails.
    """
    retained_rails = [
        rail
        for rail in (config.rails or [])
        if not isinstance(rail, WebToolRoutingRail)
        and not (
            isinstance(rail, SkillUseRail)
            and rail.enabled_skills == {OPENCLI_WEB_SKILL_NAME}
        )
    ]
    routing_rails = build_web_agent_routing_rails(
        skills_dir=skills_dir,
        disabled_skills=disabled_skills,
    )
    config.rails = [*retained_rails, *routing_rails] or None


__all__ = [
    "OPENCLI_WEB_SKILL_NAME",
    "build_web_agent_config",
    "build_web_agent_routing_rails",
    "refresh_web_agent_routing_rails",
]
