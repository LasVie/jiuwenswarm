---
opencli_contract:
  version: 2
  site: twitter
  operation: write-actions
  policy_sha256: d3dfdd9f50e334a4672153f072546b8d93fc2b4c68dc2786edab05aea347b96c
  commands:
    accept:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Keywords to match (comma-separated for OR, e.g. "群,微信")
        name: query
        positional: true
        required: true
        type: string
      - default: 20
        help: 'Maximum number of requests to accept (default: 20)'
        name: max
        required: false
        type: int
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
    list-add:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Numeric ID of the list you own (e.g. from `opencli twitter lists`)
        name: listId
        positional: true
        required: true
        type: string
      - help: Twitter/X handle to add (with or without @)
        name: username
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
    list-add-batch:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Numeric ID of the list you own (e.g. from `opencli twitter lists`)
        name: listId
        positional: true
        required: true
        type: string
      - help: Comma-separated Twitter/X handles to add (with or without @)
        name: usernames
        positional: true
        required: true
        type: string
      - default: 5
        help: 'Seconds to wait between account additions (default: 5)'
        name: interval
        required: false
        type: int
      - default: 600
        help: 'Max seconds for the overall batch command (default: 600)'
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
    quote:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: The URL of the tweet to quote
        name: url
        positional: true
        required: true
        type: string
      - help: The text content of your quote
        name: text
        positional: true
        required: true
        type: string
      - help: Optional local image path to attach to the quote tweet
        name: image
        required: false
        type: str
      - help: Optional remote image URL to download and attach to the quote tweet
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
    retweet:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: The URL of the tweet to retweet
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
    unblock:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Twitter screen name (without @)
        name: username
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
    unbookmark:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Tweet URL to unbookmark
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
    unlike:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: The URL of the tweet to unlike
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
    unretweet:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: The URL of the tweet to unretweet
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
---

# Twitter: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `accept` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Auto-accept DM requests containing specific keywords | `query` (string, required, positional); `max` (int, optional, default=20); `timeout` (int, optional, default=600) |
| `list-add` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Add a user to a Twitter/X list you own (no-op if already a member) | `listId` (string, required, positional); `username` (string, required, positional) |
| `list-add-batch` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Add multiple users to a Twitter/X list you own from a comma-separated username list | `listId` (string, required, positional); `usernames` (string, required, positional); `interval` (int, optional, default=5); `timeout` (int, optional, default=600) |
| `quote` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Quote-tweet a specific tweet with your own text, optionally with a local or remote image | `url` (string, required, positional); `text` (string, required, positional); `image` (str, optional); `image-url` (str, optional) |
| `retweet` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Retweet a specific tweet | `url` (string, required, positional) |
| `unblock` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Unblock a Twitter user | `username` (string, required, positional) |
| `unbookmark` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Remove a tweet from bookmarks | `url` (string, required, positional) |
| `unlike` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Remove a like from a specific tweet | `url` (string, required, positional) |
| `unretweet` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Undo a retweet on a specific tweet | `url` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
