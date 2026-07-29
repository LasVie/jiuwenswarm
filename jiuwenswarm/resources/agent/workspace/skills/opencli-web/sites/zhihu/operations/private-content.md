---
opencli_contract:
  version: 2
  site: zhihu
  operation: private-content
  policy_sha256: 55ef63e4ab56270a7bf67acaaf6364d6ae74c524f167bbcdf0acfa3a33547520
  commands:
    collection:
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
      - help: 收藏夹 ID (数字，可从收藏夹 URL 中获取)
        name: id
        positional: true
        required: true
        type: str
      - default: 0
        help: 起始偏移量（用于分页）
        name: offset
        required: false
        type: int
      - default: 20
        help: 每页数量（最大 20）
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
      - private social content
      - account identifiers
    collections:
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
        help: 每页数量（最大 20）
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
      - private social content
      - account identifiers
    recommend:
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
        help: Number of items to return (max 1000; use normal-sized requests)
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
      - private social content
      - account identifiers
---

# Zhihu: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `collection` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎收藏夹内容列表（需要登录） | `id` (str, required, positional); `offset` (int, optional, default=0); `limit` (int, optional, default=20) |
| `collections` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎收藏夹列表（需要登录） | `limit` (int, optional, default=20) |
| `recommend` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎首页推荐 | `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
