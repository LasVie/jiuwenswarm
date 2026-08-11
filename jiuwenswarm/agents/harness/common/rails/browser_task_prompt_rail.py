# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Extend SubagentRail's task_tool section with browser delegation rules."""

from __future__ import annotations

from openjiuwen.core.single_agent.rail.base import AgentCallbackContext
from openjiuwen.harness.rails import SubagentRail

from jiuwenswarm.agents.harness.common.prompt.browser_task_prompt import (
    build_browser_task_prompt_extension,
)


class BrowserTaskPromptRail(SubagentRail):
    """Keep browser invocation guidance inside the standard task_tool section."""

    priority = 95

    def __init__(
        self,
        channel: str = "web",
        enable_async_subagent: bool = False,
    ) -> None:
        self._channel = self._normalize_channel(channel)
        super().__init__(
            enable_async_subagent=enable_async_subagent,
            task_prompt_extension=self._task_prompt_extension,
        )

    def set_channel(self, channel: str | None) -> None:
        """Update the request channel used by the next model call."""
        self._channel = self._normalize_channel(channel)

    def _task_prompt_extension(
        self,
        _ctx: AgentCallbackContext,
        _language: str,
    ) -> str | None:
        """Return Browser guidance through agent-core's task prompt extension."""
        if self._channel != "web":
            return None
        return build_browser_task_prompt_extension()

    @staticmethod
    def _normalize_channel(channel: str | None) -> str:
        return str(channel or "web").strip().lower() or "web"
