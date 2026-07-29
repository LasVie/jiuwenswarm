---
opencli_contract:
  version: 2
  site: tiktok
  operation: private-content
  policy_sha256: 3442947251dff64808dcca780e0776b04a96d6a79525a6606459b850e8bbc53f
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
      - creator analytics
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
      - social graph
      - account identifiers
    friends:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: optional
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
      - personalized recommendations
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
      - private notifications
      - account identifiers
---

# Tiktok: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `creator-videos` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>TikTok Studio creator content list (views/likes/comments/saves/shares) | `limit` (int, optional, default=20); `cursor` (string, optional, default='0') |
| `following` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List accounts the logged-in user follows on TikTok via page-context APIs | `limit` (int, optional, default=20) |
| `friends` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get TikTok friend / who-to-follow suggestions via page-context APIs | `limit` (int, optional, default=20) |
| `notifications` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read TikTok inbox notifications (likes, comments, mentions, followers) via page-context APIs | `limit` (int, optional, default=15); `type` (str, optional, default='all', choices=all,likes,comments,mentions,followers) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
