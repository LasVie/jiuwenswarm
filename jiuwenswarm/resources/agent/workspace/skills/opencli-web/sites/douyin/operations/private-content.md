---
opencli_contract:
  version: 2
  site: douyin
  operation: private-content
  policy_sha256: 44a88f4e2945603337450f4d82e1d94d30556064265afb43719f582edd8ebf4c
  commands:
    activities:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
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
      - default: 20
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
    hashtag:
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
      - choices:
        - search
        - suggest
        - hot
        help: search=关键词搜索 (--keyword 必填), suggest=AI推荐 (--cover 必填), hot=热点词 (--keyword 可选)
        name: action
        positional: true
        required: true
        type: str
      - default: ''
        help: 搜索关键词. search 必填; hot 可选; suggest 不使用 (传 --cover)
        name: keyword
        required: false
        type: str
      - default: ''
        help: 封面 URI (cover_uri). suggest 必填; 其它 action 不使用
        name: cover
        required: false
        type: str
      - default: 10
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
    stats:
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
      - help: 抖音作品 ID（aweme_id，可从作品 URL 末尾获取）
        name: aweme_id
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
    videos:
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
        help: 每页数量
        name: limit
        required: false
        type: int
      - default: 1
        help: 页码
        name: page
        required: false
        type: int
      - choices:
        - all
        - published
        - reviewing
        - scheduled
        default: all
        help: ''
        name: status
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

# Douyin: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `activities` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>官方活动列表 | none |
| `collections` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>合集列表 | `limit` (int, optional, default=20) |
| `drafts` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取草稿列表 | `limit` (int, optional, default=20) |
| `hashtag` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>话题搜索 / AI推荐 / 热点词 | `action` (str, required, positional, choices=search,suggest,hot); `keyword` (str, optional, default=''); `cover` (str, optional, default=''); `limit` (int, optional, default=10) |
| `stats` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>作品数据分析 | `aweme_id` (str, required, positional) |
| `videos` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取作品列表 | `limit` (int, optional, default=20); `page` (int, optional, default=1); `status` (str, optional, default='all', choices=all,published,reviewing,scheduled) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
