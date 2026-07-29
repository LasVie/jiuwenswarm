---
opencli_contract:
  version: 2
  site: chatgpt
  operation: generation
  policy_sha256: 28d35bad52983e014ac34c237dbe49d3a4dafdf31f0d1339e061d5a2c581c990
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
      - help: Continue an existing ChatGPT conversation ID or /c/<id> URL
        name: conversation
        required: false
        type: str
        valueRequired: true
      - help: Start a new chat inside a ChatGPT project ID or /g/g-p-<id> URL
        name: project
        required: false
        type: str
        valueRequired: true
      - default: true
        help: Wait for the assistant response after sending
        name: wait
        required: false
        type: boolean
      - default: false
        help: Enable ChatGPT 深度研究 (Deep Research)
        name: deep-research
        required: false
        type: boolean
      - default: false
        help: Enable ChatGPT 网页搜索 (Web Search)
        name: web-search
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
      - help: Image prompt to send to ChatGPT
        name: prompt
        positional: true
        required: true
        type: str
      - help: Local image path to attach before prompting; comma-separated paths are supported
        name: image
        required: false
        type: str
      - help: Start image generation inside a ChatGPT project ID or /g/g-p-<id> URL
        name: project
        required: false
        type: str
        valueRequired: true
      - help: 'Output directory (default: ~/Pictures/chatgpt)'
        name: op
        required: false
        type: str
      - default: false
        help: Skip download shorthand; only show ChatGPT link
        name: sd
        required: false
        type: boolean
      - default: 240
        help: 'Max seconds for the overall command (default: 240)'
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
      args:
      - help: Start a new chat inside a ChatGPT project ID or /g/g-p-<id> URL
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
---

# Chatgpt: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ask` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Send a prompt to ChatGPT web and wait for the response | `prompt` (str, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False); `conversation` (str, optional); `project` (str, optional); `wait` (boolean, optional, default=True); `deep-research` (boolean, optional, default=False); `web-search` (boolean, optional, default=False) |
| `image` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Generate images with ChatGPT web and save them locally | `prompt` (str, required, positional); `image` (str, optional); `project` (str, optional); `op` (str, optional); `sd` (boolean, optional, default=False); `timeout` (int, optional, default=240) |
| `new` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Start a new ChatGPT web conversation | `project` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
