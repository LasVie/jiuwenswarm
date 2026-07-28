---
opencli_contract:
  version: 2
  site: pixiv
  operation: private-content
  policy_sha256: e9303e047b7b72047b963ed3369498fc39abe1ac1d606327b7342cbeb779ad33
  commands:
    detail:
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
      - help: Illustration ID
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
    illusts:
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    ranking:
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
      - help: Pixiv user ID
        name: uid
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
---

# Pixiv: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>View illustration details (tags, stats, URLs) | `id` (str, required, positional) |
| `illusts` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List a Pixiv artist's illustrations | `user-id` (str, required, positional); `limit` (int, optional, default=20) |
| `ranking` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Pixiv illustration rankings (daily/weekly/monthly) | `mode` (str, optional, default='daily', choices=daily,weekly,monthly,rookie,original,male,female,daily_r18,weekly_r18); `page` (int, optional, default=1); `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search Pixiv illustrations by keyword | `query` (str, required, positional); `limit` (int, optional, default=20); `order` (str, optional, default='date_d', choices=date_d,date,popular_d,popular_male_d,popular_female_d); `mode` (str, optional, default='all', choices=all,safe,r18); `page` (int, optional, default=1) |
| `user` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>View Pixiv artist profile | `uid` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
