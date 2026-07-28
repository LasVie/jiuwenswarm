---
opencli_contract:
  version: 2
  site: deepseek
  operation: messaging
  policy_sha256: 6302061dd41f35107ea7fe65b087496214ae1ac9cc1f529117a030d8427c993d
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
      - help: Conversation ID (UUID) or full /a/chat/s/<id> URL
        name: id
        positional: true
        required: true
        type: str
      - help: Prompt to send
        name: prompt
        positional: true
        required: true
        type: str
      - default: 60
        help: 'Max seconds for the overall command (default: 60)'
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
---

# Deepseek: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `send` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Send a prompt to a specific DeepSeek conversation by ID, without waiting for a response | `id` (str, required, positional); `prompt` (str, required, positional); `timeout` (int, optional, default=60) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
