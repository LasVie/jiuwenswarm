---
opencli_contract:
  version: 2
  site: twitter
  operation: account
  policy_sha256: d3dfdd9f50e334a4672153f072546b8d93fc2b4c68dc2786edab05aea347b96c
  commands:
    profile:
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
      - help: Twitter screen name (with or without @). Defaults to the logged-in user when omitted.
        name: username
        positional: true
        required: false
        type: string
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

# Twitter: account

Read account identity or account-scoped metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `profile` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch a Twitter user profile — bio, stats, etc. (defaults to the logged-in user when no username is given) | `username` (string, optional, positional) |
| `whoami` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show the current logged-in twitter account | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
