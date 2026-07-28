---
opencli_contract:
  version: 2
  site: kimi
  operation: private-content
  policy_sha256: 056583a5f1c52cef59531c9069f8800486317741e706b3dc0a99070b53dabbaa
  commands:
    cookies:
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
      - help: Chat ID or full /chat/<id> URL
        name: id
        positional: true
        required: true
        type: str
      - default: 20
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
      - private content
      - account identifiers
    history:
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
      - default: 30
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
      - private content
      - account identifiers
    idb-list:
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
      - help: Chat id or URL (navigates there before reading)
        name: conv
        required: false
        type: str
      - default: 20
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
      - private content
      - account identifiers
    status:
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
    storage-get:
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
      - help: Storage key
        name: key
        positional: true
        required: true
        type: str
      - default: local
        help: ''
        name: storage
        required: false
        type: str
      - default: 4000
        help: ''
        name: max-bytes
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
    storage-keys:
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
      - default: local
        help: '"local" or "session"'
        name: storage
        required: false
        type: str
      - help: Case-insensitive substring filter over keys
        name: filter
        required: false
        type: str
      - default: 100
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
      - private content
      - account identifiers
    templates:
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
      - help: 'Navigate to mode first: ppt|docs|deep-research|agent|websites|sheets|agent-swarm|code'
        name: mode
        required: false
        type: str
      - default: 30
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
      - private content
      - account identifiers
    usage:
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
---

# Kimi: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `cookies` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List kimi.com cookies visible to JavaScript (httpOnly cookies are deliberately not shown). | none |
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Open a Kimi chat by ID and return its visible messages. | `id` (str, required, positional); `limit` (int, optional, default=20) |
| `history` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List recent Kimi chats from the sidebar (with chat IDs extracted from href). | `limit` (int, optional, default=30) |
| `idb-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List IndexedDB databases on kimi.com. | none |
| `read` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read messages in the current Kimi chat. Pass --conv <id> to navigate to a specific chat first. | `conv` (str, optional); `limit` (int, optional, default=20) |
| `status` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Check Kimi page connection, login state, and current URL. | none |
| `storage-get` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read a single localStorage / sessionStorage value on kimi.com. Auto-decodes JSON. | `key` (str, required, positional); `storage` (str, optional, default='local'); `max-bytes` (int, optional, default=4000) |
| `storage-keys` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List localStorage / sessionStorage keys on kimi.com (with byte sizes). | `storage` (str, optional, default='local'); `filter` (str, optional); `limit` (int, optional, default=100) |
| `templates` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List template cards visible on a Kimi mode page (PPT/docs/deep-research/agent). Each mode shows curated example projects organized by category. Pass --mode to navigate first. | `mode` (str, optional); `limit` (int, optional, default=30) |
| `usage` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read Kimi Code console usage cards: weekly quota, rate limit, membership, and model permission. | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
