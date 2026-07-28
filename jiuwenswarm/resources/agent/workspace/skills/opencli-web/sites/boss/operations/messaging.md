---
opencli_contract:
  version: 2
  site: boss
  operation: messaging
  policy_sha256: 7bf0146c4d09d643b06c584dccd0f48d8b22e84aa66a69872e0757c0841e48a5
  commands:
    invite:
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
      - help: Encrypted UID of the candidate
        name: uid
        positional: true
        required: true
        type: str
      - help: Interview time (e.g. 2025-04-01 14:00)
        name: time
        required: true
        type: str
      - default: ''
        help: Interview address (uses saved address if empty)
        name: address
        required: false
        type: str
      - default: ''
        help: Contact person name (uses saved contact if empty)
        name: contact
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
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
      - help: Encrypted UID of the candidate (from chatlist)
        name: uid
        positional: true
        required: true
        type: str
      - help: Message text to send
        name: text
        positional: true
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

# Boss: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `invite` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>BOSS直聘发送面试邀请 | `uid` (str, required, positional); `time` (str, required); `address` (str, optional, default=''); `contact` (str, optional, default='') |
| `send` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>BOSS直聘发送聊天消息 | `uid` (str, required, positional); `text` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
