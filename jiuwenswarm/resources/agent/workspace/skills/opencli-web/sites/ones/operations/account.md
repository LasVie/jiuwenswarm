---
opencli_contract:
  version: 2
  site: ones
  operation: account
  policy_sha256: 027a99dcb0f14b2fc236d75acfd6d1fc3f25ea66e37eed3c88a977a52859ca03
  commands:
    me:
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

# Ones: account

Read account identity or account-scoped metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `me` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>ONES Project API — current user (GET users/me) via Chrome Bridge | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
