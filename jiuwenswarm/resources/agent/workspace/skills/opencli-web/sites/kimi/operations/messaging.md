---
opencli_contract:
  version: 2
  site: kimi
  operation: messaging
  policy_sha256: 06589d724fcc28aebeb0e534d47ba40ca82b10436b9126fb01a38ef3b18467a7
  commands:
    copy-message:
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
      - help: Chat id or URL (navigates there before reading)
        name: conv
        required: false
        type: str
      - default: false
        help: Also click in-UI Copy button (writes to clipboard)
        name: click-button
        required: false
        type: boolean
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
      - help: Message text
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

# Kimi: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `copy-message` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Return the text of the last assistant message. Pass --conv <id> to navigate to a specific chat first. | `conv` (str, optional); `click-button` (boolean, optional, default=False) |
| `send` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Send a message in the current Kimi chat (fire-and-forget; does not wait for reply). | `text` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
