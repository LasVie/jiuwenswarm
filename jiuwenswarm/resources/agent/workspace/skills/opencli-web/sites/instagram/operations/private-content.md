---
opencli_contract:
  version: 2
  site: instagram
  operation: private-content
  policy_sha256: 2f23b0dffc95b6eb1f0ec9f5697f887ee9af073f197122b3280c07425989434d
  commands:
    followers:
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
      - help: Instagram username
        name: username
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of followers
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
      - help: Instagram username
        name: username
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of accounts
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
      - default: 20
        help: Number of saved posts
        name: limit
        required: false
        type: int
      - help: Collection name (case-insensitive). Omit for the default "All posts" feed.
        name: collection
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - saved content
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
      - help: Instagram username
        name: username
        positional: true
        required: true
        type: str
      - default: 12
        help: Number of posts
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
      - private social content
      - account identifiers
---

# Instagram: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `followers` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List followers of an Instagram user | `username` (str, required, positional); `limit` (int, optional, default=20) |
| `following` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List accounts an Instagram user is following | `username` (str, required, positional); `limit` (int, optional, default=20) |
| `saved` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get your saved Instagram posts (optionally from a specific collection) | `limit` (int, optional, default=20); `collection` (str, optional) |
| `user` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get recent posts from an Instagram user | `username` (str, required, positional); `limit` (int, optional, default=12) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
