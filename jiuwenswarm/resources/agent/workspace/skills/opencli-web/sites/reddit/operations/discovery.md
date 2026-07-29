---
opencli_contract:
  version: 2
  site: reddit
  operation: discovery
  policy_sha256: b899e066532b76d45800f057c889f9dfb932b03bd7979cb0b6f4ad4af9b71596
  commands:
    frontpage:
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
      - default: 15
        help: ''
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
      - default: ''
        help: Subreddit name (e.g. programming). Empty for frontpage
        name: subreddit
        required: false
        type: str
      - default: 20
        help: Number of posts
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
    popular:
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
        help: ''
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
      - help: Reddit search query
        name: query
        positional: true
        required: true
        type: string
      - default: ''
        help: Search within a specific subreddit
        name: subreddit
        required: false
        type: string
      - default: relevance
        help: 'Sort order: relevance, hot, top, new, comments'
        name: sort
        required: false
        type: string
      - default: all
        help: 'Time filter: hour, day, week, month, year, all'
        name: time
        required: false
        type: string
      - default: 15
        help: ''
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
    subreddit:
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
      - help: Subreddit name (no `r/` prefix; e.g. `python`)
        name: name
        positional: true
        required: true
        type: string
      - default: hot
        help: 'Sorting method: hot, new, top, rising, controversial'
        name: sort
        required: false
        type: string
      - default: all
        help: 'Time filter for top/controversial: hour, day, week, month, year, all'
        name: time
        required: false
        type: string
      - default: 15
        help: ''
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

# Reddit: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `frontpage` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Reddit Frontpage / r/all | `limit` (int, optional, default=15) |
| `hot` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Reddit 热门帖子 | `subreddit` (str, optional, default=''); `limit` (int, optional, default=20) |
| `popular` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Reddit Popular posts (/r/popular) | `limit` (int, optional, default=20) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Search Reddit Posts | `query` (string, required, positional); `subreddit` (string, optional, default=''); `sort` (string, optional, default='relevance'); `time` (string, optional, default='all'); `limit` (int, optional, default=15) |
| `subreddit` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get posts from a specific Subreddit | `name` (string, required, positional); `sort` (string, optional, default='hot'); `time` (string, optional, default='all'); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
