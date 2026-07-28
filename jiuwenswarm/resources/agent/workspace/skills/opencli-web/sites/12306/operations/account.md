---
opencli_contract:
  version: 2
  site: '12306'
  operation: account
  policy_sha256: b7f15f19feca7a98b1b695a65d7139aac92e1fa3b74e98b53577a248b8718321
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
      args:
      - default: false
        help: Reveal unmasked real name / email / mobile / birth date. The 12306 ID-number mask is server-side and never decoded.
        name: include-sensitive
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
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

# 12306: account

Read account identity or account-scoped metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `me` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show the logged-in 12306 account summary. Sensitive fields (real name, email, mobile, birth date) are masked by default; pass --include-sensitive to opt in. | `include-sensitive` (boolean, optional, default=False) |
| `whoami` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show the current logged-in 12306 account | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
