---
opencli_contract:
  version: 2
  site: manus
  operation: authentication
  policy_sha256: ead9e408bf508b78a88509fc9bff3a898e40fedf1bf5ae290c3888092b0176b6
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
      - default: 300
        help: Maximum seconds to wait for the user to finish login
        name: timeout
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Manus: authentication

Open, change, or clear an authenticated browser session.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `login` | `disabled` | `auth_session_change` / `high` | Not executable; use the declared fallback if permitted<br>Open manus login and wait until the browser session is authenticated | `timeout` (int, optional, default=300) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
