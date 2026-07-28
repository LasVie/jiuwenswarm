---
opencli_contract:
  version: 2
  site: tieba
  operation: private-content
  policy_sha256: dcada3ba5d18c8a20a69e25d8507686a5e1b571d0c8ba764dbbcca6d0861101b
  commands:
    hot:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
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
      - help: Forum name in Chinese
        name: forum
        positional: true
        required: true
        type: string
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
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
    read:
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
      - help: Thread ID
        name: id
        positional: true
        required: true
        type: string
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
      - default: 30
        help: Number of replies to return
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
        name: keyword
        positional: true
        required: true
        type: string
      - choices:
        - '1'
        default: 1
        help: Page number (currently only 1 is supported)
        name: page
        required: false
        type: int
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
---

# Tieba: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Tieba hot topics | `limit` (int, optional, default=20) |
| `posts` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Browse posts in a tieba forum | `forum` (string, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20) |
| `read` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read a tieba thread | `id` (string, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=30) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search posts across tieba | `keyword` (string, required, positional); `page` (int, optional, default=1, choices=1); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
