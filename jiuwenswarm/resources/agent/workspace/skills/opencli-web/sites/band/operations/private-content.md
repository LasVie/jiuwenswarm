---
opencli_contract:
  version: 2
  site: band
  operation: private-content
  policy_sha256: 341937abc18a2b45d045de1962ef7452ac908f234ea7aaeeaa24279cc34a79d7
  commands:
    bands:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    mentions:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_intercept
      strategy: intercept
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - choices:
        - mentioned
        - all
        - post
        - comment
        default: mentioned
        help: 'Filter: mentioned (default) | all | post | comment'
        name: filter
        required: false
        type: str
      - default: 20
        help: Max results
        name: limit
        required: false
        type: int
      - default: false
        help: Show only unread notifications
        name: unread
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    post:
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
      - help: Band number
        name: band_no
        positional: true
        required: true
        type: int
      - help: Post number
        name: post_no
        positional: true
        required: true
        type: int
      - default: ''
        help: Directory to save attached photos
        name: output
        required: false
        type: str
      - default: true
        help: 'Include comments (default: true)'
        name: comments
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    posts:
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
      - help: 'Band number (get it from: band bands)'
        name: band_no
        positional: true
        required: true
        type: int
      - default: 20
        help: Max results
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

# Band: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `bands` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List all Bands you belong to | none |
| `mentions` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show Band notifications where you are @mentioned | `filter` (str, optional, default='mentioned', choices=mentioned,all,post,comment); `limit` (int, optional, default=20); `unread` (bool, optional, default=False) |
| `post` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Export full content of a post including comments | `band_no` (int, required, positional); `post_no` (int, required, positional); `output` (str, optional, default=''); `comments` (bool, optional, default=True) |
| `posts` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List posts from a Band | `band_no` (int, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
