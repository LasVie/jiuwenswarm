---
opencli_contract:
  version: 2
  site: jike
  operation: private-content
  policy_sha256: f05c6947bf8b738be4ec401e0cae980808f3b984f8d6143c3bf0e4ac951e3323
  commands:
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
    notifications:
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
    post:
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
      - help: Post ID (from post URL)
        name: id
        positional: true
        required: true
        type: string
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
      - help: 即刻搜索关键词
        name: query
        positional: true
        required: true
        type: string
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
      - help: Topic ID (from topic URL, e.g. 553870e8e4b0cafb0a1bef68)
        name: id
        positional: true
        required: true
        type: string
      - default: 20
        help: Number of posts
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
    user:
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
      - help: Username from profile URL (e.g. wenhao1996)
        name: username
        positional: true
        required: true
        type: string
      - default: 20
        help: Number of posts
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

# Jike: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `feed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>即刻首页动态流 | `limit` (int, optional, default=20) |
| `notifications` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>即刻通知 | `limit` (int, optional, default=20) |
| `post` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>即刻帖子详情及评论 | `id` (string, required, positional) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>搜索即刻帖子 | `query` (string, required, positional); `limit` (int, optional, default=20) |
| `topic` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>即刻话题/圈子帖子 | `id` (string, required, positional); `limit` (int, optional, default=20) |
| `user` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>即刻用户动态 | `username` (string, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
