---
opencli_contract:
  version: 2
  site: rednote
  operation: private-content
  policy_sha256: e74eb27b8de6e5cfbe7c9e82937ac7994460405b9d6ab27989389a959792e5bc
  commands:
    comments:
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
      - help: Full rednote note URL with xsec_token
        name: note-id
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of top-level comments (max 50)
        name: limit
        required: false
        type: int
      - default: false
        help: Include nested replies (楼中楼)
        name: with-replies
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    feed:
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
    note:
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
      - help: Full rednote note URL with xsec_token
        name: note-id
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
      - default: mentions
        help: 'Notification type: mentions, likes, or connections'
        name: type
        required: false
        type: str
      - default: 20
        help: Number of notifications to return
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
      - help: Search keyword
        name: query
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
      - help: User id or profile URL
        name: id
        positional: true
        required: true
        type: str
      - default: 15
        help: Number of notes to return
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

# Rednote: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comments` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read comments from a rednote note (supports nested replies) | `note-id` (str, required, positional); `limit` (int, optional, default=20); `with-replies` (boolean, optional, default=False) |
| `feed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Rednote home feed (reads hydrated Pinia store) | `limit` (int, optional, default=20) |
| `note` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read note body and engagement counts from a rednote note | `note-id` (str, required, positional) |
| `notifications` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Rednote notifications (mentions/likes/connections) | `type` (str, optional, default='mentions'); `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search rednote notes | `query` (str, required, positional); `limit` (int, optional, default=20) |
| `user` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get public notes from a rednote user profile | `id` (str, required, positional); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
