---
opencli_contract:
  version: 2
  site: gemini
  operation: generation
  policy_sha256: 73a86fcade69579b88c656ba09a4fe558916bb2b16dbb4a875f17703931af580
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
      - help: Gemini model to use (e.g. "2.5-flash"). Use "opencli gemini models" to list available values.
        name: model
        required: false
        type: string
      - default: 60
        help: 'Max seconds to wait (default: 60)'
        name: timeout
        required: false
        type: int
      - default: 'false'
        help: 'Start a new chat first (true/false, default: false)'
        name: new
        required: false
        type: str
      - default: null
        help: 'Thinking level: standard or extended (omitted = leave unchanged)'
        name: thinking
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    deep-research:
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
      - default: 180
        help: 'Max seconds for the overall command (default: 180; confirm-wait clamps internally to 6-20s)'
        name: timeout
        required: false
        type: int
      - help: 'Override tool label (default: Deep Research)'
        name: tool
        required: false
        type: str
      - help: 'Override confirm button label (default: Start research)'
        name: confirm
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    deep-research-result:
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
      - help: Conversation title or URL (optional; defaults to latest conversation)
        name: query
        positional: true
        required: false
        type: str
      - choices:
        - contains
        - exact
        default: contains
        help: Match mode
        name: match
        required: false
        type: str
      - default: 120
        help: 'Max seconds to wait for Docs export (default: 120)'
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
      - help: Image prompt to send to Gemini
        name: prompt
        positional: true
        required: true
        type: str
      - default: '1:1'
        help: Ratio shorthand for aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3)
        name: rt
        required: false
        type: str
      - default: ''
        help: Style shorthand, e.g. anime, icon, watercolor
        name: st
        required: false
        type: str
      - default: ~/tmp/gemini-images
        help: Output directory shorthand
        name: op
        required: false
        type: str
      - default: false
        help: Skip download shorthand; only show Gemini page link
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Gemini: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ask` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Send a prompt to Gemini and return only the assistant response | `prompt` (str, required, positional); `model` (string, optional); `timeout` (int, optional, default=60); `new` (str, optional, default='false'); `thinking` (str, optional, default=None) |
| `deep-research` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Start a Gemini Deep Research run and confirm it | `prompt` (str, required, positional); `timeout` (int, optional, default=180); `tool` (str, optional); `confirm` (str, optional) |
| `deep-research-result` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Export Deep Research report URL from a Gemini conversation | `query` (str, optional, positional); `match` (str, optional, default='contains', choices=contains,exact); `timeout` (int, optional, default=120) |
| `image` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Generate images with Gemini web and save them locally | `prompt` (str, required, positional); `rt` (str, optional, default='1:1'); `st` (str, optional, default=''); `op` (str, optional, default='~/tmp/gemini-images'); `sd` (boolean, optional, default=False); `timeout` (int, optional, default=240) |
| `new` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Start a new conversation in Gemini web chat | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
