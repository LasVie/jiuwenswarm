---
opencli_contract:
  version: 2
  site: hupu
  operation: private-content
  policy_sha256: 86a3ddfcf16b3fc55407f3ac6dca5cc09098caa7777218d355d2b7e11cea3261
  commands:
    mentions:
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
      - default: 20
        help: 最多返回多少条消息
        name: limit
        required: false
        type: int
      - default: 3
        help: 最多抓取多少页
        name: max_pages
        required: false
        type: int
      - help: 分页游标；不传时从第一页开始
        name: page_str
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private notifications
      - account identifiers
---

# Hupu: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `mentions` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>查看虎扑提到我的回复 (需要登录) | `limit` (int, optional, default=20); `max_pages` (int, optional, default=3); `page_str` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
