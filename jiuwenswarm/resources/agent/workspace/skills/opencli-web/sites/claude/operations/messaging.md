---
opencli_contract:
  version: 2
  site: claude
  operation: messaging
  policy_sha256: 44e3058291e9515c11b69fa315716c43953b92c95d540a39de4eb5d2af4eb50d
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
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Claude: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `send` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Send a prompt to Claude without waiting for the response | `prompt` (str, required, positional); `new` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
