---
opencli_contract:
  version: 2
  site: grok
  operation: destructive-actions
  policy_sha256: b705477e7e3a3a6973224daa59302383677bcd142ed82fafc4864ece1d1486a2
  commands:
    delete:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Conversation UUID or grok.com/c/<uuid> URL
        name: id
        positional: true
        required: true
        type: string
      - default: false
        help: Actually delete (default is a dry-run preview)
        name: 'yes'
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Grok: destructive-actions

Delete, remove, revoke, or perform administrative changes.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `delete` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Delete a Grok conversation by ID. Grok takes effect immediately with no confirmation dialog — require --yes to actually delete. | `id` (string, required, positional); `yes` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
