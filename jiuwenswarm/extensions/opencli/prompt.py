# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.
"""Routing prompt appended to the Browser Agent when site commands are enabled."""

from __future__ import annotations

from jiuwenswarm.extensions.opencli.catalog import Catalog

_CN = """# 站点命令（OpenCLI）

下列站点有现成的命令，可以直接拿到结构化结果，比逐步操作页面更快：
{sites}

使用规则：
1. 任务涉及上面的站点时，先用 opencli_describe 查看该站点的命令；有适用的命令就用 opencli_run 执行，没有再用页面工具。
2. 命令只覆盖部分步骤时，按步骤组合两种工具；页面工具接手某一步之后，后续步骤仍可回到命令。两者使用不同的页面，接续只依赖 URL、业务 ID 和共享的登录态。
3. 用户明确要求打开页面、截图或在页面上核对时，这一步用页面工具完成，例如打开命令结果中的 URL。
4. 上文关于观察页面、probe、构造搜索 URL 的指引只在使用页面工具时适用。
5. opencli_run 返回 reason=needs_user 时，不要用页面工具绕过验证，直接结束任务，并把结果里的处理说明原样转告（用户需要在侧栏「OpenCLI」标签页处理，然后点击「已完成，继续」）。
6. 写命令由用户在侧栏确认。结果为 executed=unknown 时，先用读命令或页面核实；不得重复提交，也不要换页面工具重做。
7. opencli_describe 列出待核实的写操作时，执行同类写操作之前先核实。"""

_EN = """# Site commands (OpenCLI)

These sites have ready-made commands that return structured results faster than operating the page step by step:
{sites}

Rules:
1. When the task involves a site above, call opencli_describe for that site first; if a command fits, run it with opencli_run, otherwise use the page tools.
2. When commands cover only part of the task, combine both tools step by step; after the page tools take over a step, later steps may return to commands. They use different pages, so hand-offs rely only on URLs, business IDs and the shared sign-in state.
3. When the user explicitly asks to open a page, take a screenshot or check something on the page, do that step with the page tools, for example by opening a URL from the command result.
4. The guidance above about observing pages, probes and building search URLs applies only when you use the page tools.
5. When opencli_run returns reason=needs_user, do not try to get around the check with the page tools. End the task and pass the result's instructions on verbatim (the user acts in the sidebar's OpenCLI tab, then clicks "Done, continue").
6. The user confirms write commands in the sidebar. When a result has executed=unknown, verify with a read command or the page first; never resubmit, and do not redo it with the page tools.
7. When opencli_describe lists unverified writes, verify them before running the same kind of write again."""


def build_routing_prompt(catalog: Catalog, language: str = "cn") -> str:
    template = _EN if language == "en" else _CN
    separator = ", " if language == "en" else "、"
    return template.format(sites=separator.join(catalog.sites()))
