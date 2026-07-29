---
opencli_contract:
  version: 2
  site: bilibili
  operation: private-content
  policy_sha256: 6e8e73109dd43108bc96445fe5fb962e20e71bd5fabb4922fa485aa95e9accb6
  commands:
    dynamic:
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
      - default: 15
        help: ''
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
    feed:
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
      - help: 用户 UID 或用户名（不传则显示关注时间线）
        name: uid
        positional: true
        required: false
        type: str
      - default: 20
        help: Max results to return
        name: limit
        required: false
        type: int
      - default: all
        help: 'Filter: all, video, article, draw, text'
        name: type
        required: false
        type: str
      - default: 1
        help: Number of pages to fetch (each ~20 items)
        name: pages
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
    feed-detail:
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
      - help: 动态 ID（从 feed 命令的 url 中获取）
        name: id
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    following:
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
      - help: 目标用户 ID（默认为当前登录用户）
        name: uid
        positional: true
        required: false
        type: str
      - default: 1
        help: 页码
        name: page
        required: false
        type: int
      - default: 50
        help: 每页数量 (最大 50)
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
    history:
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
        help: Number of results
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

# Bilibili: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `dynamic` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get Bilibili user dynamic feed | `limit` (int, optional, default=15) |
| `feed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>动态时间线（不传 uid 查关注时间线，传 uid 查指定用户动态） | `uid` (str, optional, positional); `limit` (int, optional, default=20); `type` (str, optional, default='all'); `pages` (int, optional, default=1) |
| `feed-detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>查看 Bilibili 动态详情（支持充电专属内容） | `id` (str, required, positional) |
| `following` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取 Bilibili 用户的关注列表 | `uid` (str, optional, positional); `page` (int, optional, default=1); `limit` (int, optional, default=50) |
| `history` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>我的观看历史 | `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
