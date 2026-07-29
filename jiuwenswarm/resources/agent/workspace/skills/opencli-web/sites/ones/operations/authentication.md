---
opencli_contract:
  version: 2
  site: ones
  operation: authentication
  policy_sha256: 64d44ee783edfb380e515b610ab3f68cdc26d3c6e52d68eae4e61b20a8f378e0
  commands:
    login:
      executor: none
      execution_state: disabled
      semantic_effect: auth_session_change
      risk: high
      auth: interactive
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Account email (or set ONES_EMAIL)
        name: email
        required: false
        type: str
      - help: Account phone (or set ONES_PHONE); ignored if email is set
        name: phone
        required: false
        type: str
      - help: Password (or set ONES_PASSWORD)
        name: password
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    logout:
      executor: none
      execution_state: disabled
      semantic_effect: auth_session_change
      risk: high
      auth: interactive
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Ones: authentication

Open, change, or clear an authenticated browser session.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `login` | `disabled` | `auth_session_change` / `high` | Not executable; use the declared fallback if permitted<br>ONES Project API — login via Chrome Bridge (POST auth/login); stderr prints export hints for ONES_USER_ID / TOKEN | `email` (str, optional); `phone` (str, optional); `password` (str, optional) |
| `logout` | `disabled` | `auth_session_change` / `high` | Not executable; use the declared fallback if permitted<br>ONES Project API — invalidate current token (GET auth/logout) via Chrome Bridge | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
