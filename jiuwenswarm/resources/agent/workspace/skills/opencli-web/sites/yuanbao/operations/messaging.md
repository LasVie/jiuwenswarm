---
opencli_contract:
  version: 2
  site: yuanbao
  operation: messaging
  policy_sha256: 286e0ea8163a76cd0781de943293e8e2959bad09793d1c0fd15cacfd2581539c
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
      - help: Prompt to send to Yuanbao
        name: prompt
        positional: true
        required: true
        type: str
      - default: false
        help: Start a new chat before sending
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
---

# Yuanbao: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `send` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Fire-and-forget: send a prompt to Yuanbao without waiting for the reply | `prompt` (str, required, positional); `new` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
