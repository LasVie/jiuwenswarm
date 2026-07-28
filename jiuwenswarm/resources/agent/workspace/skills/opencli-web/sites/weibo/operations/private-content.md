---
opencli_contract:
  version: 2
  site: weibo
  operation: private-content
  policy_sha256: ad9fe9aad5f989b83f399caba4b2e7a2cb38fc789078e5f2ab7ddcbd9f56e44b
  commands:
    comments:
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
      - help: Post ID (numeric idstr)
        name: id
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of comments (max 50)
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
    favorites:
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
        help: 数量（最多50）
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
      - choices:
        - for-you
        - following
        default: for-you
        help: 'Timeline type: for-you (algorithmic) or following (chronological)'
        name: type
        required: false
        type: str
      - default: 15
        help: Number of posts (max 50)
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
    hot:
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
      - default: 30
        help: Number of items (max 50)
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
      - help: Post ID (numeric idstr or mblogid from URL)
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
      - default: 10
        help: Number of results (max 50)
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
      - help: User ID (numeric uid) or screen name
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
    user-posts:
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
      - help: User ID (numeric uid) or screen name
        name: id
        positional: true
        required: true
        type: str
      - help: Start date in Asia/Shanghai (YYYY-MM-DD)
        name: start
        required: false
        type: str
      - help: End date in Asia/Shanghai (YYYY-MM-DD)
        name: end
        required: false
        type: str
      - default: 20
        help: Number of posts (1-100)
        name: limit
        required: false
        type: int
      - default: false
        help: Include retweets
        name: include-retweets
        required: false
        type: boolean
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

# Weibo: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comments` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get comments on a Weibo post | `id` (str, required, positional); `limit` (int, optional, default=20) |
| `favorites` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>我的微博收藏列表 | `limit` (int, optional, default=20) |
| `feed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch Weibo timeline (for-you or following) | `type` (str, optional, default='for-you', choices=for-you,following); `limit` (int, optional, default=15) |
| `hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>微博热搜 | `limit` (int, optional, default=30) |
| `post` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get a single Weibo post | `id` (str, required, positional) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>搜索微博 | `keyword` (str, required, positional); `limit` (int, optional, default=10) |
| `user` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get Weibo user profile | `id` (str, required, positional) |
| `user-posts` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List Weibo posts from a user, optionally filtered by date range | `id` (str, required, positional); `start` (str, optional); `end` (str, optional); `limit` (int, optional, default=20); `include-retweets` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
