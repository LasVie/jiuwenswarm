# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Inject the OpenCLI-first Web tool routing policy."""

from __future__ import annotations

from openjiuwen.core.single_agent.rail.base import AgentCallbackContext
from openjiuwen.harness.rails.base import DeepAgentRail

from jiuwenswarm.agents.harness.common.prompt.web_tool_routing_prompt import (
    WEB_TOOL_ROUTING_SECTION,
    build_web_tool_routing_prompt,
)


class WebToolRoutingRail(DeepAgentRail):
    """Own routing decisions between OpenCLI and browser_agent on Web requests."""

    priority = 94
    _LEGACY_SECTIONS = ("opencli_web_policy", "browser_tool_policy")

    def __init__(self, channel: str = "web") -> None:
        super().__init__()
        self.system_prompt_builder = None
        self._channel = self._normalize_channel(channel)

    def init(self, agent) -> None:
        self.system_prompt_builder = getattr(agent, "system_prompt_builder", None)

    def uninit(self, agent) -> None:
        self._remove_sections()
        self.system_prompt_builder = None

    def set_channel(self, channel: str | None) -> None:
        """Update the request channel used by the next model call."""
        self._channel = self._normalize_channel(channel)

    async def before_model_call(self, ctx: AgentCallbackContext) -> None:
        if self.system_prompt_builder is None:
            return

        self._remove_sections()
        if self._channel == "web":
            self.system_prompt_builder.add_section(build_web_tool_routing_prompt())

    def _remove_sections(self) -> None:
        if self.system_prompt_builder is None:
            return
        self.system_prompt_builder.remove_section(WEB_TOOL_ROUTING_SECTION)
        for name in self._LEGACY_SECTIONS:
            self.system_prompt_builder.remove_section(name)

    @staticmethod
    def _normalize_channel(channel: str | None) -> str:
        return str(channel or "web").strip().lower() or "web"
