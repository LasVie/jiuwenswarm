---
opencli_contract:
  version: 2
  site: mercury
  operation: authentication
  policy_sha256: a1376e6ba8694455786c63a7039937f24f5b24f3bccff07d273186601fe14613
  commands:
    check-login:
      executor: none
      execution_state: disabled
      semantic_effect: auth_session_change
      risk: high
      auth: interactive
      transport: browser_dom
      strategy: ui
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
      sensitive_output: []
---

# Mercury: authentication

Open, change, or clear an authenticated browser session.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `check-login` | `disabled` | `auth_session_change` / `high` | Not executable; use the declared fallback if permitted<br>Open Mercury reimbursements and report whether the active browser profile is logged in | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
