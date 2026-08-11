# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Browser-specific extension for the standard task_tool prompt section."""

from __future__ import annotations


def build_browser_task_prompt_extension() -> str:
    """Describe how to invoke browser_agent after the routing rail selects it."""
    return (
        "## Browser Agent Delegation\n\n"
        "- For a browser-only task or a permitted browser fallback selected by web routing, use `task_tool` "
        "with `subagent_type` set to `\"browser_agent\"`. Put the objective in "
        "`task_description`, including opening pages, navigation, clicking, typing, login, screenshots, page "
        "inspection, or extracting data from a live website.\n"
        "- Do not use bash, execute_code, subprocess, shell commands, or direct Chrome/Edge launches for "
        "browser automation. Do not launch browsers or run ad-hoc browser scripts from the shell.\n"
        "- If `task_tool` or `browser_agent` is unavailable, report that the browser subagent is unavailable "
        "instead of trying to start a browser through commands."
    )
