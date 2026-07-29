---
opencli_contract:
  version: 2
  site: zhihu
  operation: content
  policy_sha256: 55ef63e4ab56270a7bf67acaaf6364d6ae74c524f167bbcdf0acfa3a33547520
  commands:
    answer-comments:
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    answer-detail:
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    question:
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user:
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
      - help: User url_token or people URL, e.g. wen-jie-16-47
        name: user
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Zhihu: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `answer-comments` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎回答评论列表 | `id` (str, required, positional); `limit` (int, optional, default=20); `replies-limit` (int, optional, default=3) |
| `answer-detail` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎单个回答完整内容（按 answer ID 获取） | `id` (str, required, positional); `max-content` (int, optional, default=0) |
| `question` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎问题详情和回答 | `id` (str, required, positional); `limit` (int, optional, default=5); `sort` (str, optional, default='default', choices=default,created) |
| `user` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>知乎用户主页资料（粉丝/关注/回答/文章/获赞数） | `user` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
