---
opencli_contract:
  version: 2
  site: chatgpt
  operation: messaging
  policy_sha256: cbd22f6bc7157ff01dec9ec104e5e019587993a4880d14dd9c65b07c9498cf5d
  commands:
    send:
      executor: none
      execution_state: disabled
      semantic_effect: message_send
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
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Chatgpt: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `send` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Send a prompt to ChatGPT web without waiting for the response | `prompt` (str, required, positional); `new` (boolean, optional, default=False); `conversation` (str, optional); `project` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
