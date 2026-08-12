# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Parent-agent delegation contract for the Browser/Web Agent."""

from __future__ import annotations


def build_browser_task_prompt_extension() -> str:
    """Delegate live-site work once; Browser/Web Agent owns tool routing."""
    return (
        "## Browser/Web Agent Delegation\n\n"
        "- For every live-site interaction or page/account-state task, excluding discussion, local web "
        "development, and purpose-built non-browser capabilities, call `task_tool` once with "
        "`subagent_type=\"browser_agent\"`. Browser/Web Agent owns OpenCLI-first matching and its local "
        "Playwright fallback. The main agent must not read `opencli-web`, execute OpenCLI, or perform the "
        "browser operation itself.\n"
        "- Put the complete objective, URLs/IDs, constraints, relevant prior results, and explicit user "
        "approval (if any) in `task_description`; the child does not inherit the full parent conversation.\n"
        "- If it returns `confirmation_required`, obtain the user's decision with the available confirmation "
        "UI, then call the same sticky `browser_agent` again with that decision. Never treat delegation as consent.\n"
        "- If `task_tool` or `browser_agent` is unavailable, report that the browser subagent is unavailable "
        "instead of using shell commands or launching another browser."
    )
