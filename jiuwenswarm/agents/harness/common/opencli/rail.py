# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Rail that turns an exact main-Agent Skill read into an execution receipt."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from openjiuwen.core.single_agent.rail.base import (
    AgentCallbackContext,
    ToolCallInputs,
)
from openjiuwen.harness.rails.base import DeepAgentRail

from jiuwenswarm.agents.harness.common.opencli.contracts import (
    OPENCLI_WEB_SKILL_NAME,
    OpenCLIContractError,
    load_terminal_contract_by_path,
)
from jiuwenswarm.agents.harness.common.opencli.disclosure import (
    DisclosureReceiptStore,
)
from jiuwenswarm.agents.harness.common.opencli.security import (
    load_skill_enabled_snapshot,
)


class OpenCLIDisclosureRail(DeepAgentRail):
    """Issue receipts only after this Agent reads an exact operation via SkillTool."""

    priority = 101

    def __init__(
        self,
        *,
        scope: str,
        skills_root: str | Path,
        receipt_store: DisclosureReceiptStore,
        allowed_skill_directories: Sequence[str | Path] = (),
    ) -> None:
        super().__init__()
        self._scope = scope
        self._skills_root = Path(skills_root).expanduser()
        self._receipt_store = receipt_store
        self._allowed_skill_directories = tuple(allowed_skill_directories)

    async def after_tool_call(self, ctx: AgentCallbackContext) -> None:
        inputs = ctx.inputs
        if not isinstance(inputs, ToolCallInputs):
            return
        if str(inputs.tool_name or "").strip() != "skill_tool":
            return

        args = self._mapping(inputs.tool_args)
        if args.get("skill_name") != OPENCLI_WEB_SKILL_NAME:
            return
        relative_path = str(args.get("relative_file_path") or "")

        result = self._mapping(inputs.tool_result)
        if result.get("success") is not True:
            return
        data = self._mapping(result.get("data"))
        skill_directory = str(data.get("skill_directory") or "").strip()
        skill_content = data.get("skill_content")
        if not skill_directory or not isinstance(skill_content, str):
            return

        installed_skill_root = (self._skills_root / OPENCLI_WEB_SKILL_NAME).resolve()
        allowed_skill_directories = {installed_skill_root}
        for directory in self._allowed_skill_directories:
            try:
                allowed_skill_directories.add(Path(directory).expanduser().resolve())
            except (OSError, RuntimeError, ValueError):
                continue
        try:
            result_skill_root = Path(skill_directory).expanduser().resolve()
        except (OSError, RuntimeError, ValueError):
            return
        if result_skill_root not in allowed_skill_directories:
            return

        enabled_snapshot = load_skill_enabled_snapshot(self._skills_root)
        if not enabled_snapshot.enabled:
            return
        try:
            contract = load_terminal_contract_by_path(
                self._skills_root,
                relative_path,
            )
        except OpenCLIContractError:
            return
        if not any(
            command.execution_state in {"enabled", "custom"}
            and command.executor != "none"
            for command in contract.command_specs.values()
        ):
            return
        disclosed_sha256 = hashlib.sha256(skill_content.encode("utf-8")).hexdigest()
        if disclosed_sha256 != contract.terminal_sha256:
            return

        self._receipt_store.grant_bound(
            scope=self._scope,
            site=contract.site,
            operation=contract.operation,
            terminal_relative_path=contract.terminal_relative_path,
            terminal_sha256=contract.terminal_sha256,
            policy_sha256=contract.policy_sha256,
            enabled_state_sha256=enabled_snapshot.state_sha256,
        )

    @staticmethod
    def _mapping(value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return value
        model_dump = getattr(value, "model_dump", None)
        if callable(model_dump):
            dumped = model_dump()
            return dumped if isinstance(dumped, dict) else {}
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except (TypeError, ValueError):
                return {}
            return parsed if isinstance(parsed, dict) else {}
        return {}


__all__ = ["OpenCLIDisclosureRail"]
