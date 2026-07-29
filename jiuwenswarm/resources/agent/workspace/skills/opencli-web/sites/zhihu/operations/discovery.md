---
opencli_contract:
  version: 2
  site: zhihu
  operation: discovery
  policy_sha256: 55ef63e4ab56270a7bf67acaaf6364d6ae74c524f167bbcdf0acfa3a33547520
  commands:
    followers:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    following:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    hot:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    pins:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user-answers:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user-articles:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Zhihu: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `followers` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎某用户的粉丝列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |
| `following` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎某用户关注的人列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |
| `hot` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎热榜 | `limit` (int, optional, default=20) |
| `pins` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎某用户的想法（短内容）列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎搜索 | `query` (str, required, positional); `limit` (int, optional, default=10); `type` (str, optional, default='all', choices=all,answer,article,question) |
| `user-answers` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎某用户的回答列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |
| `user-articles` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎某用户的文章/专栏列表 | `user` (string, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
