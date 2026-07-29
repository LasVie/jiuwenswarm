---
opencli_contract:
  version: 2
  site: claude
  operation: generation
  policy_sha256: ea0df9e9268dc8d38770a9fee8900e554e09d12e27deda8d74693b7d9447db94
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
        name: prompt
        positional: true
        required: true
        type: str
      - default: 120
        help: Max seconds to wait for response
        name: timeout
        required: false
        type: int
      - default: false
        help: Start a new chat before sending
        name: new
        required: false
        type: boolean
      - choices:
        - sonnet
        - opus
        - haiku
        default: sonnet
        help: 'Model to use: sonnet, opus, or haiku'
        name: model
        required: false
        type: str
      - default: false
        help: Enable Adaptive thinking
        name: think
        required: false
        type: boolean
      - help: Attach a file (image, PDF, text) with the prompt
        name: file
        required: false
        type: str
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

# Claude: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ask` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Send a prompt to Claude and get the response | `prompt` (str, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False); `model` (str, optional, default='sonnet', choices=sonnet,opus,haiku); `think` (boolean, optional, default=False); `file` (str, optional) |
| `new` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Start a new conversation in Claude | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
