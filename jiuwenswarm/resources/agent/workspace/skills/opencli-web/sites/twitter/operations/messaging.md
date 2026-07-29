---
opencli_contract:
  version: 2
  site: twitter
  operation: messaging
  policy_sha256: ea1c61e10694164a7221301d4eb1fd14fec218da88d65957161ff72d1a564726
  commands:
    hide-reply:
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
      - help: The URL of the reply tweet to hide
        name: url
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    reply:
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
      - help: The URL of the tweet to reply to
        name: url
        positional: true
        required: true
        type: string
      - help: The text content of your reply
        name: text
        positional: true
        required: true
        type: string
      - help: Optional local image path to attach to the reply
        name: image
        required: false
        type: str
      - help: Optional remote image URL to download and attach to the reply
        name: image-url
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    reply-dm:
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
      - help: Message text to send (e.g. "我的微信 wxkabi")
        name: text
        positional: true
        required: true
        type: string
      - default: 20
        help: 'Maximum number of conversations to reply to (default: 20)'
        name: max
        required: false
        type: int
      - default: true
        help: 'Skip conversations where you already sent the same text (default: true)'
        name: skip-replied
        required: false
        type: boolean
      - default: 600
        help: 'Max seconds for the overall command (default: 600 — batch op)'
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

# Twitter: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hide-reply` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Hide a reply on your tweet (useful for hiding bot/spam replies) | `url` (string, required, positional) |
| `reply` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Reply to a specific tweet, optionally with a local or remote image | `url` (string, required, positional); `text` (string, required, positional); `image` (str, optional); `image-url` (str, optional) |
| `reply-dm` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>Send a message to recent DM conversations | `text` (string, required, positional); `max` (int, optional, default=20); `skip-replied` (boolean, optional, default=True); `timeout` (int, optional, default=600) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
