# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Routing prompt appended to the Browser Agent when site commands are enabled."""

from __future__ import annotations

from jiuwenswarm.extensions.opencli.catalog import Catalog

_CN = """# 站点命令（OpenCLI）

下列站点有现成的命令，可以直接拿到结构化结果，比逐步操作页面更快：
{sites}

使用规则：
1. 任务涉及上面的站点时（即使任务里写了该站点的网址），先用 opencli_describe 查一次该站点：结果已包含全部命令及参数，不要再逐个命令查询；有适用的命令就直接用 opencli_run 执行，没有再用页面工具。
2. 命令返回了任务要求的数据时，直接用这些数据完成任务，不要再打开页面重新采集或核对；只有用户明确要求查看、截图或在页面上核对，或命令结果缺少要求的字段时，才使用页面工具。
3. 命令只覆盖部分步骤时，按步骤组合两种工具；页面工具接手某一步之后，后续步骤仍可回到命令。两者使用不同的页面，接续只依赖 URL、业务 ID 和共享的登录态。
4. 用户明确要求打开页面、截图或在页面上核对时，这一步用页面工具完成，例如打开命令结果中的 URL。
5. 上文关于观察页面、probe、构造搜索 URL 的指引只在使用页面工具时适用。
6. opencli_run 返回 reason=needs_user 时，不要用页面工具绕过验证，直接结束任务，并把结果里的处理说明原样转告（用户需要在侧栏「OpenCLI」标签页处理，然后点击「已完成，继续」）。
7. 写命令由用户在侧栏确认。结果为 executed=unknown 时，先用读命令或页面核实；不得重复提交，也不要换页面工具重做。
8. opencli_describe 列出待核实的写操作时，执行同类写操作之前先核实。"""

_EN = """# Site commands (OpenCLI)

These sites have ready-made commands that return structured results faster than operating the page step by step:
{sites}

Rules:
1. When the task involves a site above (even if the task gives that site's URL), call opencli_describe once for that site: the result already lists every command with its arguments, so do not look up commands one by one. If a command fits, run it directly with opencli_run; otherwise use the page tools.
2. When a command returns the data the task asks for, complete the task from that data; do not open the page to collect or check it again. Use the page tools only when the user explicitly asks to see, screenshot or check the page, or when the command result lacks a required field.
3. When commands cover only part of the task, combine both tools step by step; after the page tools take over a step, later steps may return to commands. They use different pages, so hand-offs rely only on URLs, business IDs and the shared sign-in state.
4. When the user explicitly asks to open a page, take a screenshot or check something on the page, do that step with the page tools, for example by opening a URL from the command result.
5. The guidance above about observing pages, probes and building search URLs applies only when you use the page tools.
6. When opencli_run returns reason=needs_user, do not try to get around the check with the page tools. End the task and pass the result's instructions on verbatim (the user acts in the sidebar's OpenCLI tab, then clicks "Done, continue").
7. The user confirms write commands in the sidebar. When a result has executed=unknown, verify with a read command or the page first; never resubmit, and do not redo it with the page tools.
8. When opencli_describe lists unverified writes, verify them before running the same kind of write again."""


_CARD_CN = (
    "另有现成的站点命令（OpenCLI），可直接返回结构化结果，覆盖：{sites}。"
    "涉及这些站点的任务（搜索、读取、发布，或用户提到 adapter、站点命令）应主动交给本代理，"
    "由它自行查找合适的命令；这些命令不在主代理的工具目录中。"
)
_CARD_EN = (
    "Also has ready-made site commands (OpenCLI) that return structured results for: {sites}. "
    "Delegate tasks on these sites (searching, reading, posting, or requests that mention an adapter or "
    "site command) to this agent proactively; it finds the right command itself. These commands are not "
    "in the main agent's tool directory."
)
# The card goes into the parent agent's subagent list, so keep it short.
CARD_SITE_LIMIT = 30


def build_routing_prompt(catalog: Catalog, language: str = "cn") -> str:
    template = _EN if language == "en" else _CN
    separator = ", " if language == "en" else "、"
    return template.format(sites=separator.join(catalog.sites()))


def build_card_note(catalog: Catalog, language: str = "cn") -> str:
    """Sentence appended to the Browser Agent's card so the parent agent knows to delegate."""
    sites = list(catalog.sites())
    shown = sites[:CARD_SITE_LIMIT]
    if language == "en":
        text = ", ".join(shown)
        if len(sites) > len(shown):
            text += f" and {len(sites) - len(shown)} more"
        return _CARD_EN.format(sites=text)
    text = "、".join(shown)
    if len(sites) > len(shown):
        text += f" 等 {len(sites)} 个站点"
    return _CARD_CN.format(sites=text)
