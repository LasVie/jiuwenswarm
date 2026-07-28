---
opencli_contract:
  version: 2
  site: doubao
  operation: generation
  policy_sha256: 497429c0c2f48886ea1c123aede806adc056daf1f8b180b9e402c44a988dd96a
  commands:
    ask:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Prompt to send
        name: text
        positional: true
        required: true
        type: str
      - default: 60
        help: 'Max seconds to wait (default: 60)'
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
    new:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
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
      sensitive_output: []
---

# Doubao: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ask` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Send a prompt and wait for the Doubao response | `text` (str, required, positional); `timeout` (int, optional, default=60) |
| `new` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Start a new conversation in Doubao web chat | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
