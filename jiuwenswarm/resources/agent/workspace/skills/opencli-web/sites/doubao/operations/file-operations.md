---
opencli_contract:
  version: 2
  site: doubao
  operation: file-operations
  policy_sha256: 497429c0c2f48886ea1c123aede806adc056daf1f8b180b9e402c44a988dd96a
  commands:
    meeting-transcript:
      executor: none
      execution_state: disabled
      semantic_effect: local_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Conversation ID (numeric or full URL)
        name: id
        positional: true
        required: true
        type: str
      - default: 'false'
        help: Trigger browser file download instead of reading text
        name: download
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs:
      - workspace-relative output
      sensitive_output: []
---

# Doubao: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `meeting-transcript` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Get or download the meeting transcript from a Doubao conversation | `id` (str, required, positional); `download` (str, optional, default='false') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
