---
opencli_contract:
  version: 2
  site: chatgpt
  operation: private-content
  policy_sha256: 28d35bad52983e014ac34c237dbe49d3a4dafdf31f0d1339e061d5a2c581c990
  commands:
    deep-research-result:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Conversation ID or full /c/<id> URL
        name: id
        positional: true
        required: true
        type: str
      - default: false
        help: Wait until Deep Research completes or becomes extractable
        name: wait
        required: false
        type: boolean
      - default: 120
        help: Max seconds to wait when --wait is true
        name: timeout
        required: false
        type: int
      - default: 6
        help: Seconds the report text must remain unchanged when --wait is true
        name: stable
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private conversation content
      - account identifiers
    detail:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Conversation ID or full /c/<id> URL
        name: id
        positional: true
        required: true
        type: str
      - default: false
        help: Emit assistant replies as markdown
        name: markdown
        required: false
        type: boolean
      - default: false
        help: Wait until the conversation stops generating and stabilizes
        name: wait
        required: false
        type: boolean
      - default: 120
        help: Max seconds to wait when --wait is true
        name: timeout
        required: false
        type: int
      - default: 6
        help: Seconds the final messages must remain unchanged when --wait is true
        name: stable
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private conversation content
      - account identifiers
    history:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Max conversations to show
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
      - private conversation content
      - account identifiers
    project-list:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Max projects to show
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
      - private project metadata
      - account identifiers
    read:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: false
        help: Emit assistant replies as markdown
        name: markdown
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private conversation content
      - account identifiers
---

# Chatgpt: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `deep-research-result` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read a completed ChatGPT Deep Research report from the conversation payload | `id` (str, required, positional); `wait` (boolean, optional, default=False); `timeout` (int, optional, default=120); `stable` (int, optional, default=6) |
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Open a ChatGPT web conversation by ID and read its messages | `id` (str, required, positional); `markdown` (boolean, optional, default=False); `wait` (boolean, optional, default=False); `timeout` (int, optional, default=120); `stable` (int, optional, default=6) |
| `history` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List visible ChatGPT web conversation history from the sidebar | `limit` (int, optional, default=20) |
| `project-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List visible ChatGPT projects from the sidebar | `limit` (int, optional, default=20) |
| `read` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read messages in the current ChatGPT web conversation | `markdown` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
