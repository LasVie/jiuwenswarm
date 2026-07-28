---
opencli_contract:
  version: 2
  site: zhihu
  operation: private-content
  policy_sha256: 72cfde1a8e42b9be48a1414fe1c119c65782c8b4c07c241be09bd6fcad8a4929
  commands:
    answer-comments:
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
      - help: Answer ID, full Zhihu answer URL, or typed target (answer:<qid>:<aid>)
        name: id
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of top-level comments (max 1000)
        name: limit
        required: false
        type: int
      - default: 3
        help: Number of replies to include per top-level comment (max 100)
        name: replies-limit
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
    answer-detail:
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
      - help: Answer ID, full Zhihu answer URL, or typed target (answer:<qid>:<aid>)
        name: id
        positional: true
        required: true
        type: str
      - default: 0
        help: Optional cap on stripped content length in characters (0 = no truncation, return the full answer)
        name: max-content
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
      - private content
      - account identifiers
    followers:
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
      - help: User url_token or people URL
        name: user
        positional: true
        required: true
        type: string
      - default: 20
        help: Number of followers to return (max 1000)
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
      - help: User url_token or people URL
        name: user
        positional: true
        required: true
        type: string
      - default: 20
        help: Number of followees to return (max 1000)
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
      - default: 20
        help: Number of items to return
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
    pins:
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
      - help: User url_token or people URL
        name: user
        positional: true
        required: true
        type: string
      - default: 20
        help: Number of pins to return (max 1000)
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
    question:
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
      - help: Question ID (numeric)
        name: id
        positional: true
        required: true
        type: str
      - default: 5
        help: Number of answers (max 1000; use normal-sized requests)
        name: limit
        required: false
        type: int
      - choices:
        - default
        - created
        default: default
        help: 'Answer order: default or created'
        name: sort
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
      - help: Search query
        name: query
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of results (max 1000; use normal-sized requests)
        name: limit
        required: false
        type: int
      - choices:
        - all
        - answer
        - article
        - question
        default: all
        help: 'Result type: all, answer, article, or question'
        name: type
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
      - help: User url_token or people URL, e.g. wen-jie-16-47
        name: user
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
    user-answers:
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
      - help: User url_token or people URL
        name: user
        positional: true
        required: true
        type: string
      - default: 20
        help: Number of answers to return (max 1000)
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
    user-articles:
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
      - help: User url_token or people URL
        name: user
        positional: true
        required: true
        type: string
      - default: 20
        help: Number of articles to return (max 1000)
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

# Zhihu: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `answer-comments` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎回答评论列表 | `id` (str, required, positional); `limit` (int, optional, default=20); `replies-limit` (int, optional, default=3) |
| `answer-detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎单个回答完整内容（按 answer ID 获取） | `id` (str, required, positional); `max-content` (int, optional, default=0) |
| `collection` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎收藏夹内容列表（需要登录） | `id` (str, required, positional); `offset` (int, optional, default=0); `limit` (int, optional, default=20) |
| `collections` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎收藏夹列表（需要登录） | `limit` (int, optional, default=20) |
| `followers` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎某用户的粉丝列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |
| `following` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎某用户关注的人列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |
| `hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎热榜 | `limit` (int, optional, default=20) |
| `pins` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎某用户的想法（短内容）列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |
| `question` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎问题详情和回答 | `id` (str, required, positional); `limit` (int, optional, default=5); `sort` (str, optional, default='default', choices=default,created) |
| `recommend` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎首页推荐 | `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎搜索 | `query` (str, required, positional); `limit` (int, optional, default=10); `type` (str, optional, default='all', choices=all,answer,article,question) |
| `user` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎用户主页资料（粉丝/关注/回答/文章/获赞数） | `user` (string, required, positional) |
| `user-answers` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎某用户的回答列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |
| `user-articles` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>知乎某用户的文章/专栏列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
