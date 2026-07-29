---
opencli_contract:
  version: 2
  site: weibo
  operation: discovery
  policy_sha256: 17339ca0c0792c7964caf7e12e245c79ae3efdb2806901b9b89aee69e0f359ea
  commands:
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
      - default: 30
        help: Number of items (max 50)
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user-posts:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Weibo: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hot` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>微博热搜 | `limit` (int, optional, default=30) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>搜索微博 | `keyword` (str, required, positional); `limit` (int, optional, default=10) |
| `user-posts` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>List Weibo posts from a user, optionally filtered by date range | `id` (str, required, positional); `start` (str, optional); `end` (str, optional); `limit` (int, optional, default=20); `include-retweets` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
