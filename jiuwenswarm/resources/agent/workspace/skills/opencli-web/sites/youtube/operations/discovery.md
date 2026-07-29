---
opencli_contract:
  version: 2
  site: youtube
  operation: discovery
  policy_sha256: 3d5906cc99870a2ef1d70a87acc167b81f0397a620e41320bd3ec7bc994d1617
  commands:
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
      - default: 20
        help: Max results (max 50)
        name: limit
        required: false
        type: int
      - default: ''
        help: 'Filter type: shorts, video, channel, playlist'
        name: type
        required: false
        type: str
      - default: ''
        help: 'Upload date: hour, today, week, month, year'
        name: upload
        required: false
        type: str
      - default: ''
        help: 'Sort by: relevance, date, views, rating'
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
---

# Youtube: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Search YouTube videos | `query` (str, required, positional); `limit` (int, optional, default=20); `type` (str, optional, default=''); `upload` (str, optional, default=''); `sort` (str, optional, default='') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
