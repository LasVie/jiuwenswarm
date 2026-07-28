---
opencli_contract:
  version: 2
  site: slock
  operation: messaging
  policy_sha256: 3b7327b298620fa16c0e1582c663796bbfffa42b1e4d50d6695d895b572bf804
  commands:
    message-send:
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
      - help: '"#channel", "#channel:msgIdOrShort", "dm:@name", "dm:<uuid>", or channel UUID'
        name: target
        positional: true
        required: true
        type: str
      - help: Message body (sent verbatim, no marker)
        name: content
        positional: true
        required: true
        type: str
      - default: false
        help: Print the planned payload without sending
        name: dry-run
        required: false
        type: bool
      - default: false
        help: Create the message as a task (asTask)
        name: as-task
        required: false
        type: bool
      - help: Comma-separated attachmentId UUIDs (upload separately first)
        name: attach
        required: false
        type: str
      - help: Override active server (slug or id)
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Slock: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `message-send` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Send a message to a channel, DM, or thread (content sent verbatim) | `target` (str, required, positional); `content` (str, required, positional); `dry-run` (bool, optional, default=False); `as-task` (bool, optional, default=False); `attach` (str, optional); `server` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
