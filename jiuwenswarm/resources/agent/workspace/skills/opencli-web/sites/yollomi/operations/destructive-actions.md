---
opencli_contract:
  version: 2
  site: yollomi
  operation: destructive-actions
  policy_sha256: ee2545bccbf6c52893001c0918b7503f043bcac13306e93647f8fc8ce9b8d5e2
  commands:
    remove-bg:
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
      - help: Image URL to remove background from
        name: image
        positional: true
        required: true
        type: str
      - default: ./yollomi-output
        help: Output directory
        name: output
        required: false
        type: str
      - default: false
        help: Only show URL
        name: no-download
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

# Yollomi: destructive-actions

Delete, remove, revoke, or perform administrative changes.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `remove-bg` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Remove image background with AI (free) | `image` (str, required, positional); `output` (str, optional, default='./yollomi-output'); `no-download` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
