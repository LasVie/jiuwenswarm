---
opencli_contract:
  version: 2
  site: grok
  operation: generation
  policy_sha256: d2b9f216523df47c74346d35cb34510ffe498aaed3167575f8992f4716317e63
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
      - help: Prompt to send to Grok
        name: prompt
        positional: true
        required: true
        type: string
      - default: 120
        help: 'Max seconds to wait for response (default: 120)'
        name: timeout
        required: false
        type: int
      - default: false
        help: 'Start a new chat before sending (default: false)'
        name: new
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
      - help: Image generation prompt
        name: prompt
        positional: true
        required: true
        type: string
      - default: 240
        help: 'Max seconds to wait for the image (default: 240)'
        name: timeout
        required: false
        type: int
      - default: false
        help: 'Start a new chat before sending (default: false)'
        name: new
        required: false
        type: boolean
      - default: 1
        help: 'Minimum images to wait for before returning (default: 1)'
        name: count
        required: false
        type: int
      - default: ''
        help: Directory to save downloaded images (uses browser session to bypass auth)
        name: out
        required: false
        type: string
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

# Grok: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ask` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Send a message to Grok and get response | `prompt` (string, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False) |
| `image` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Generate images on grok.com and return image URLs | `prompt` (string, required, positional); `timeout` (int, optional, default=240); `new` (boolean, optional, default=False); `count` (int, optional, default=1); `out` (string, optional, default='') |
| `new` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Start a new conversation in Grok | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
