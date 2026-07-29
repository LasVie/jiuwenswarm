---
opencli_contract:
  version: 2
  site: kimi
  operation: account
  policy_sha256: 06589d724fcc28aebeb0e534d47ba40ca82b10436b9126fb01a38ef3b18467a7
  commands:
    account:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
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
      - account identifiers
    cookies:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: high
      auth: optional
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
      - browser cookies
      - account identifiers
    idb-list:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: optional
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
      - browser storage metadata
      - account identifiers
    status:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: optional
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
      - authentication state
    storage-get:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: high
      auth: optional
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
      - browser storage values
      - account identifiers
    storage-keys:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: high
      auth: optional
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
      - browser storage metadata
      - account identifiers
    usage:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
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
      - subscription and quota data
      - account identifiers
    whoami:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
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
      - account identifiers
---

# Kimi: account

Read account identity or account-scoped metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `account` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read account info from the Kimi sidebar (display name + plan label, e.g. "Allegretto"). | none |
| `cookies` | `disabled` | `private_account_read` / `high` | Not executable; use the declared fallback if permitted<br>List kimi.com cookies visible to JavaScript (httpOnly cookies are deliberately not shown). | none |
| `idb-list` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>List IndexedDB databases on kimi.com. | none |
| `status` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Check Kimi page connection, login state, and current URL. | none |
| `storage-get` | `disabled` | `private_account_read` / `high` | Not executable; use the declared fallback if permitted<br>Read a single localStorage / sessionStorage value on kimi.com. Auto-decodes JSON. | `key` (str, required, positional); `storage` (str, optional, default='local'); `max-bytes` (int, optional, default=4000) |
| `storage-keys` | `disabled` | `private_account_read` / `high` | Not executable; use the declared fallback if permitted<br>List localStorage / sessionStorage keys on kimi.com (with byte sizes). | `storage` (str, optional, default='local'); `filter` (str, optional); `limit` (int, optional, default=100) |
| `usage` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read Kimi Code console usage cards: weekly quota, rate limit, membership, and model permission. | none |
| `whoami` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show the current logged-in kimi account | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
