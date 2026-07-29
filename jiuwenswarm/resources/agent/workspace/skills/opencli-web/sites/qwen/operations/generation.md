---
opencli_contract:
  version: 2
  site: qwen
  operation: generation
  policy_sha256: fcf84febb19f60002d518f7b57d2495d9364756134b1c42546f8d2aedae33154
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
      - help: Prompt to send to Qianwen
        name: prompt
        positional: true
        required: true
        type: str
      - default: 120
        help: Max seconds to wait for the response
        name: timeout
        required: false
        type: int
      - default: false
        help: Start a new chat before sending
        name: new
        required: false
        type: boolean
      - default: false
        help: Enable 深度思考 (DeepThink)
        name: think
        required: false
        type: boolean
      - default: false
        help: Enable 深度研究 (DeepResearch)
        name: research
        required: false
        type: boolean
      - default: false
        help: Emit assistant reply as markdown
        name: markdown
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    image:
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
      - help: Image prompt to send
        name: prompt
        positional: true
        required: true
        type: str
      - default: ~/Pictures/qianwen
        help: Output directory
        name: op
        required: false
        type: str
      - default: true
        help: 'Start a new chat before generating (default: true)'
        name: new
        required: false
        type: boolean
      - default: false
        help: Skip download; only show the Qianwen link
        name: sd
        required: false
        type: boolean
      - default: 180
        help: Max seconds to wait for the image response
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
      access: write
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Qwen: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ask` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Send a prompt to Qianwen and return the assistant reply | `prompt` (str, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False); `think` (boolean, optional, default=False); `research` (boolean, optional, default=False); `markdown` (boolean, optional, default=False) |
| `image` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Generate images with Qianwen (AI生图) and save them locally | `prompt` (str, required, positional); `op` (str, optional, default='~/Pictures/qianwen'); `new` (boolean, optional, default=True); `sd` (boolean, optional, default=False); `timeout` (int, optional, default=180) |
| `new` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Start a new conversation in Qianwen | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
