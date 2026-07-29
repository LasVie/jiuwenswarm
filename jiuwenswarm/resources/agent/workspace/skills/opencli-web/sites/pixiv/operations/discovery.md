---
opencli_contract:
  version: 2
  site: pixiv
  operation: discovery
  policy_sha256: 91fe6dcb96f651c08d5de587daada322a6f09d8257010b42751cd5ba7768c4bb
  commands:
    illusts:
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
      - help: Pixiv user ID
        name: user-id
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of results
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
    ranking:
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
      - choices:
        - daily
        - weekly
        - monthly
        - rookie
        - original
        - male
        - female
        - daily_r18
        - weekly_r18
        default: daily
        help: Ranking mode
        name: mode
        required: false
        type: str
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
      - default: 20
        help: Number of results
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
      - help: Search keyword or tag
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      - choices:
        - date_d
        - date
        - popular_d
        - popular_male_d
        - popular_female_d
        default: date_d
        help: Sort order
        name: order
        required: false
        type: str
      - choices:
        - all
        - safe
        - r18
        default: all
        help: Search mode
        name: mode
        required: false
        type: str
      - default: 1
        help: Page number
        name: page
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

# Pixiv: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `illusts` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>List a Pixiv artist's illustrations | `user-id` (str, required, positional); `limit` (int, optional, default=20) |
| `ranking` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Pixiv illustration rankings (daily/weekly/monthly) | `mode` (str, optional, default='daily', choices=daily,weekly,monthly,rookie,original,male,female,daily_r18,weekly_r18); `page` (int, optional, default=1); `limit` (int, optional, default=20) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Search Pixiv illustrations by keyword | `query` (str, required, positional); `limit` (int, optional, default=20); `order` (str, optional, default='date_d', choices=date_d,date,popular_d,popular_male_d,popular_female_d); `mode` (str, optional, default='all', choices=all,safe,r18); `page` (int, optional, default=1) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
