---
opencli_contract:
  version: 2
  site: zhihu
  operation: messaging
  policy_sha256: 72cfde1a8e42b9be48a1414fe1c119c65782c8b4c07c241be09bd6fcad8a4929
  commands:
    comment:
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
      - help: Zhihu target URL or typed target
        name: target
        positional: true
        required: true
        type: str
      - help: Comment text
        name: text
        positional: true
        required: false
        type: str
      - help: Comment text file path
        name: file
        required: false
        type: str
      - help: Actually perform the write action
        name: execute
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

# Zhihu: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comment` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Create a top-level comment on a Zhihu answer or article | `target` (str, required, positional); `text` (str, optional, positional); `file` (str, optional); `execute` (boolean, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
