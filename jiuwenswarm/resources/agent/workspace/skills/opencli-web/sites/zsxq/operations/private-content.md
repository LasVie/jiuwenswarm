---
opencli_contract:
  version: 2
  site: zsxq
  operation: private-content
  policy_sha256: 0e955abc9e8c235e9788f3fcdd59640b9a1a7605d1cf18b4b4d2c6017d264171
  commands:
    dynamics:
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
        help: Number of dynamics to return
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
    groups:
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
      - default: 50
        help: Number of groups to return
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
    search:
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
      - help: Search keyword
        name: keyword
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of results to return
        name: limit
        required: false
        type: int
      - help: Optional group id; defaults to the active group in Chrome
        name: group_id
        required: false
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
    topic:
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
      - help: Topic ID
        name: id
        positional: true
        required: true
        type: str
      - help: Group ID (optional; defaults to active group in Chrome)
        name: group_id
        required: false
        type: str
      - default: 20
        help: Number of comments to fetch
        name: comment_limit
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
    topics:
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
        help: Number of topics to return
        name: limit
        required: false
        type: int
      - help: Optional group id; defaults to the active group in Chrome
        name: group_id
        required: false
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
---

# Zsxq: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `dynamics` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取所有星球的最新动态 | `limit` (int, optional, default=20) |
| `groups` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>列出当前账号加入的星球 | `limit` (int, optional, default=50) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>搜索星球内容 | `keyword` (str, required, positional); `limit` (int, optional, default=20); `group_id` (str, optional) |
| `topic` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取单个话题详情和评论 | `id` (str, required, positional); `group_id` (str, optional); `comment_limit` (int, optional, default=20) |
| `topics` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取当前星球的话题列表 | `limit` (int, optional, default=20); `group_id` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
