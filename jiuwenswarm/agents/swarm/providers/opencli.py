# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Leader-only OpenCLI providers for declarative team assembly."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from openjiuwen.agent_teams.harness.manifest import (
    ElementKind,
    harness_element,
)

from jiuwenswarm.agents.harness.common.opencli import (
    OPENCLI_WEB_SKILL_NAME,
    OpenCLIDisclosureRail,
    OpenCLIExecuteTool,
    get_opencli_disclosure_store,
)
from jiuwenswarm.agents.swarm.context import SwarmBuildContext
from jiuwenswarm.common.utils import get_agent_skills_dir

OPENCLI_EXECUTE = "swarm.opencli_execute"
OPENCLI_DISCLOSURE = "swarm.opencli_disclosure"


def _scope(ctx: SwarmBuildContext) -> str:
    """Build a trusted receipt scope from non-model team/member identity."""
    return ":".join(
        (
            "team",
            str(ctx.session_id or "default"),
            str(ctx.team_id or "default"),
            str(ctx.member_card_id or "leader"),
        )
    )


def _skills_root(ctx: SwarmBuildContext) -> Path:
    return (
        Path(ctx.global_skills_dir)
        if ctx.global_skills_dir
        else get_agent_skills_dir()
    )


def _workspace_roots(ctx: SwarmBuildContext) -> list[Path]:
    roots: list[Path] = []
    if ctx.project_dir:
        roots.append(Path(ctx.project_dir))
    workspace_root = (
        getattr(ctx.workspace, "root_path", None)
        if ctx.workspace is not None
        else None
    )
    if workspace_root:
        roots.append(Path(workspace_root))
    if ctx.team_ws_root:
        roots.append(Path(ctx.team_ws_root))
    return roots


def _allowed_skill_directories(ctx: SwarmBuildContext) -> list[Path]:
    """Return managed Skill views from which this team leader may disclose."""
    workspace_root = (
        getattr(ctx.workspace, "root_path", None)
        if ctx.workspace is not None
        else None
    )
    if not workspace_root:
        return []
    return [
        Path(workspace_root) / "skills" / OPENCLI_WEB_SKILL_NAME,
    ]


@harness_element(
    kind=ElementKind.TOOL,
    name=OPENCLI_EXECUTE,
    description=(
        "Leader-only structured OpenCLI executor guarded by an exact operation "
        "Skill disclosure receipt."
    ),
)
def build_opencli_execute(
    params: dict[str, Any],
    ctx: SwarmBuildContext,
) -> list[OpenCLIExecuteTool]:
    """Build the stateful tool for a team leader and never for teammates."""
    del params
    if str(ctx.role or "") != "leader":
        return []
    return [
        OpenCLIExecuteTool(
            scope=_scope(ctx),
            skills_root=lambda: _skills_root(ctx),
            workspace_roots=lambda: _workspace_roots(ctx),
            receipt_store=get_opencli_disclosure_store(),
            language=str(ctx.language or "cn"),
            agent_id=str(ctx.member_card_id or "leader"),
        )
    ]


@harness_element(
    kind=ElementKind.RAIL,
    name=OPENCLI_DISCLOSURE,
    description=(
        "Leader-only rail that signs a short-lived receipt after SkillTool "
        "reads an exact executable OpenCLI operation contract."
    ),
)
def build_opencli_disclosure(
    params: dict[str, Any],
    ctx: SwarmBuildContext,
) -> OpenCLIDisclosureRail | None:
    """Build the receipt rail for a team leader and never for teammates."""
    del params
    if str(ctx.role or "") != "leader":
        return None
    return OpenCLIDisclosureRail(
        scope=_scope(ctx),
        skills_root=_skills_root(ctx),
        receipt_store=get_opencli_disclosure_store(),
        allowed_skill_directories=_allowed_skill_directories(ctx),
    )


__all__ = [
    "OPENCLI_DISCLOSURE",
    "OPENCLI_EXECUTE",
    "build_opencli_disclosure",
    "build_opencli_execute",
]
