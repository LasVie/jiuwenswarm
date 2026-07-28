---
opencli_contract:
  version: 2
  site: google-scholar
  operation: account
  policy_sha256: 0c3b32f56160b203c146f3a1e745b728787ba38836170eb583d9584a5d8e5d93
  commands:
    profile:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Author name or Scholar user ID (e.g. JicYPdAAAAAJ)
        name: author
        positional: true
        required: true
        type: str
      - default: 10
        help: Max papers to show (max 20)
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
      - account identifiers
---

# Google Scholar: account

Read account identity or account-scoped metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `profile` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>View a Google Scholar author profile | `author` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
