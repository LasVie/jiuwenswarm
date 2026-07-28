---
opencli_contract:
  version: 2
  site: linkedin
  operation: messaging
  policy_sha256: d0c16e9f75ca1a20826b14b84ed1623a5a25b38ba0d1785c847e19d8620f8018
  commands:
    connect:
      executor: none
      execution_state: disabled
      semantic_effect: message_send
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Exact LinkedIn profile URL to open and verify
        name: profile-url
        positional: true
        required: true
        type: string
      - help: Expected visible profile name
        name: expected-name
        required: true
        type: string
      - default: ''
        help: Optional connection note, max 300 chars
        name: note
        required: false
        type: string
      - default: false
        help: Actually click Send. Default is dry-run verification only.
        name: send
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    safe-send:
      executor: none
      execution_state: disabled
      semantic_effect: message_send
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Exact LinkedIn messaging thread URL to open and verify
        name: thread-url
        required: true
        type: str
      - help: Expected visible recipient name in the active thread header
        name: expected-name
        required: true
        type: str
      - help: Message body to send or dry-run
        name: message
        required: true
        type: str
      - help: Substring expected in the currently visible latest conversation context
        name: expected-last-text
        required: false
        type: str
      - help: SHA-256 hash of expected latest visible message text
        name: expected-last-hash
        required: false
        type: str
      - default: false
        help: Actually click Send. Default is dry-run verification only.
        name: send
        required: false
        type: bool
      - default: false
        help: Capture a screenshot during verification
        name: screenshot
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    salesnav-message:
      executor: none
      execution_state: disabled
      semantic_effect: message_send
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Sales Navigator lead URL, LinkedIn /in/ URL from salesnav-search, or urn:li:fs_salesProfile:(...)
        name: recipient
        positional: true
        required: true
        type: string
      - help: InMail subject
        name: subject
        required: true
        type: string
      - help: InMail body
        name: body
        required: true
        type: string
      - default: false
        help: Actually send the InMail. Default is dry-run validation only.
        name: send
        required: false
        type: bool
      - default: false
        help: Set Sales Navigator copyToCrm on the message request
        name: copy-to-crm
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Linkedin: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `connect` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Fail-closed LinkedIn connection request sender that verifies the exact profile before optionally sending a note | `profile-url` (string, required, positional); `expected-name` (string, required); `note` (string, optional, default=''); `send` (bool, optional, default=False) |
| `safe-send` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Fail-closed LinkedIn message sender that verifies exact thread, recipient, and latest message before filling/sending | `thread-url` (str, required); `expected-name` (str, required); `message` (str, required); `expected-last-text` (str, optional); `expected-last-hash` (str, optional); `send` (bool, optional, default=False); `screenshot` (bool, optional, default=False) |
| `salesnav-message` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Send or dry-run a LinkedIn Sales Navigator InMail to a lead using the Sales Navigator messaging API | `recipient` (string, required, positional); `subject` (string, required); `body` (string, required); `send` (bool, optional, default=False); `copy-to-crm` (bool, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
