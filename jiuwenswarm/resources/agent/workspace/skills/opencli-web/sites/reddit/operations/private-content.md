---
opencli_contract:
  version: 2
  site: reddit
  operation: private-content
  policy_sha256: b899e066532b76d45800f057c889f9dfb932b03bd7979cb0b6f4ad4af9b71596
  commands:
    home:
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
      - default: 25
        help: Number of posts (1–100)
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
      - personalized feed
      - account identifiers
    saved:
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
        help: ''
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
      - account activity
      - account identifiers
    subscribed:
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
      - default: 100
        help: Max subreddits to return (1-1000, auto-paginates)
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
      - account activity
      - account identifiers
    upvoted:
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
        help: ''
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
      - account activity
      - account identifiers
---

# Reddit: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `home` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Reddit personalized home feed (Best, requires login) | `limit` (int, optional, default=25) |
| `saved` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Browse your saved Reddit posts | `limit` (int, optional, default=15) |
| `subscribed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List subreddits you are subscribed to | `limit` (int, optional, default=100) |
| `upvoted` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Browse your upvoted Reddit posts | `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
