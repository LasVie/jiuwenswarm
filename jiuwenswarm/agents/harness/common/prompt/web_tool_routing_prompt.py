# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Prompt section for routing live-site work between OpenCLI and browser_agent."""

from __future__ import annotations

from openjiuwen.harness.prompts import PromptSection


WEB_TOOL_ROUTING_SECTION = "web_tool_routing"


def build_web_tool_routing_prompt() -> PromptSection:
    """Build the OpenCLI-first routing contract for Web requests."""
    content = (
        "# Web Tool Routing Policy\n\n"
        "- Scope: for live-site interaction or page/account state, use the installed, enabled "
        "`opencli-web` Skill before routing to `browser_agent`. Exclude discussion, local web development, "
        "and purpose-built non-browser capabilities; never search, install, or ask the user to select it.\n"
        "- Disclosure: the main agent alone reads the root, listed site via `relative_file_path`, then each "
        "operation needed by the task, one at a time. Use the site terminal or each operation's full listed "
        "path. No unrelated modules, `general-purpose`/`browser_agent` delegation, or filesystem reads.\n"
        "- Execution: a terminal row declares adapter capability, not readiness, authentication, or consent. "
        "Copy its exact documented command and arguments. Preserve opaque URLs, signed URLs, tokens, "
        "identifiers, and paths verbatim at execution, including query strings and fragments. Use separate "
        "shell arguments and unchanged absolute paths; prefer documented `-f json`. On Windows use "
        "`shell_type: \"auto\"`, never `bash`/`sh`.\n"
        "- Concurrency: run independent OpenCLI calls concurrently; journal and tab/session leases arbitrate "
        "persistent writes. Preserve dependencies. Never overlap `browser_agent` "
        "for the same operation or bypass `session_busy`/ambiguous writes through fallback/retry.\n"
        "- Consent: confirm `high`/`critical` and side-effecting commands with the action and material "
        "non-secret arguments, using A2UI when available. Redact credentials, tokens, and signed-URL secrets "
        "in confirmation while preserving them at execution.\n"
        "- Fallback/retry: route to `browser_agent` only if capability is absent or the terminal row permits "
        "it. `fallback_before` requires proof the adapter process did not start; if start is possible or "
        "unclear, only `fallback_after` applies. `COMMAND_EXEC` is after-start. For `ARGUMENT`, reread the "
        "contract and correct a read at most once without switching; never automatically retry writes. With "
        "`fallback_after=none`, or after a failed, timed-out, or ambiguous write, use no browser fallback; "
        "verify read-only or stop with uncertainty.\n"
    )
    return PromptSection(
        name=WEB_TOOL_ROUTING_SECTION,
        content={"cn": content, "en": content},
        priority=99,
    )
