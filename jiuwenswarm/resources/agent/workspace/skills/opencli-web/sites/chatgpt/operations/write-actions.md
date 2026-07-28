---
opencli_contract:
  version: 2
  site: chatgpt
  operation: write-actions
  policy_sha256: cbd22f6bc7157ff01dec9ec104e5e019587993a4880d14dd9c65b07c9498cf5d
  commands:
    model:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - choices:
        - fast
        - speed
        - instant
        - 极速
        - balanced
        - balance
        - medium
        - 均衡
        - advanced
        - high
        - thinking
        - 高级
        - very-high
        - ultra
        - xhigh
        - x-high
        - extra-high
        - 超高
        - pro
        - professional
        - 专业
        help: Intelligence level to switch to
        name: model
        positional: true
        required: true
        type: str
      - help: Open a ChatGPT project ID or /g/g-p-<id> URL before switching intelligence level
        name: project
        required: false
        type: str
        valueRequired: true
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    project-file-add:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Local file path(s) to upload; comma-separated paths are supported
        name: file
        positional: true
        required: true
        type: str
      - help: Project ID or /g/g-p-<id> URL
        name: id
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Chatgpt: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `model` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Switch ChatGPT web intelligence level (fast, balanced, advanced, very-high, pro) | `model` (str, required, positional, choices=fast,speed,instant,极速,balanced,balance,medium,均衡,advanced,high,thinking,高级,very-high,ultra,xhigh,x-high,extra-high,超高,pro,professional,专业); `project` (str, optional) |
| `project-file-add` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Upload files to a ChatGPT project as project knowledge (not just conversation attachments) | `file` (str, required, positional); `id` (str, required) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
