---
opencli_contract:
  version: 2
  site: tiktok
  operation: private-content
  policy_sha256: cdab1d57fbfeb8ff2fc058034ae8df793011491167265a2f7cfb61b72e773464
  commands:
    creator-videos:
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
        help: Number of creator videos to return (max 250)
        name: limit
        required: false
        type: int
      - default: '0'
        help: Non-negative TikTok Studio pagination cursor
        name: cursor
        required: false
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
    explore:
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
        help: Number of videos to return (max 120)
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
      - default: 20
        help: Number of accounts (max 200)
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
    friends:
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
        help: Number of suggestions (max 100)
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
    live:
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
      - default: 10
        help: Number of streams (max 60)
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
      - default: 15
        help: Number of notifications (max 100)
        name: limit
        required: false
        type: int
      - choices:
        - all
        - likes
        - comments
        - mentions
        - followers
        default: all
        help: Notification type
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
      - help: TikTok username (without @)
        name: username
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of videos to return (max 120)
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

# Tiktok: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `creator-videos` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>TikTok Studio creator content list (views/likes/comments/saves/shares) | `limit` (int, optional, default=20); `cursor` (string, optional, default='0') |
| `explore` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get trending TikTok videos from the recommend feed via page-context APIs | `limit` (int, optional, default=20) |
| `following` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List accounts the logged-in user follows on TikTok via page-context APIs | `limit` (int, optional, default=20) |
| `friends` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get TikTok friend / who-to-follow suggestions via page-context APIs | `limit` (int, optional, default=20) |
| `live` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Browse TikTok live streams via page-context APIs | `limit` (int, optional, default=10) |
| `notifications` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read TikTok inbox notifications (likes, comments, mentions, followers) via page-context APIs | `limit` (int, optional, default=15); `type` (str, optional, default='all', choices=all,likes,comments,mentions,followers) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search TikTok videos | `query` (str, required, positional); `limit` (int, optional, default=10) |
| `user` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get recent videos from a TikTok user via page-context APIs | `username` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
