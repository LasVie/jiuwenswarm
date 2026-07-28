---
opencli_contract:
  version: 2
  site: weixin
  operation: private-content
  policy_sha256: 4ae15f5bbeb75a3b75bca630d6636e358ee66ade40db74e20828f65545a93601
  commands:
    drafts:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 10
        help: 最多显示条数
        name: limit
        required: false
        type: int
      - default: 60
        help: 'Max seconds for the overall command (default: 60)'
        name: timeout
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    search:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 搜索关键词；如需正文 Markdown，请使用 weixin download 处理公众号文章链接
        name: query
        positional: true
        required: true
        type: str
      - default: 1
        help: 结果页码，从 1 开始
        name: page
        required: false
        type: int
      - default: 10
        help: 返回条数，最大 10
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Weixin: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `drafts` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>列出微信公众号草稿箱 | `limit` (int, optional, default=10); `timeout` (int, optional, default=60) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>使用搜狗微信搜索公众号文章；如需导出正文 Markdown，请使用 weixin download 处理公众号文章链接 | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
