---
opencli_contract:
  version: 2
  site: twitter
  operation: destructive-actions
  policy_sha256: d3dfdd9f50e334a4672153f072546b8d93fc2b4c68dc2786edab05aea347b96c
  commands:
    block:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
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
    delete:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: The URL of the tweet to delete
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
    list-delete:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
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
      - default: false
        help: Required. Set --confirm true to delete the list.
        name: confirm
        required: false
        type: boolean
      - default: 300
        help: 'Max seconds for the overall delete command (default: 300)'
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
    list-remove:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
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
      - help: Twitter/X handle to remove (with or without @)
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
    list-remove-batch:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
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
      - help: Comma-separated Twitter/X handles to remove (with or without @)
        name: usernames
        positional: true
        required: true
        type: string
      - default: 5
        help: 'Seconds to wait between account removals (default: 5)'
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
    unfollow:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
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
---

# Twitter: destructive-actions

Delete, remove, revoke, or perform administrative changes.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `block` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Block a Twitter user | `username` (string, required, positional) |
| `delete` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Delete a specific tweet by URL | `url` (string, required, positional) |
| `list-delete` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Delete a Twitter/X list you own after explicit confirmation | `listId` (string, required, positional); `confirm` (boolean, optional, default=False); `timeout` (int, optional, default=300) |
| `list-remove` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Remove a user from a Twitter/X list you own (toggles via UI; no-op if not currently a member) | `listId` (string, required, positional); `username` (string, required, positional) |
| `list-remove-batch` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Remove multiple users from a Twitter/X list you own from a comma-separated username list | `listId` (string, required, positional); `usernames` (string, required, positional); `interval` (int, optional, default=5); `timeout` (int, optional, default=600) |
| `unfollow` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Unfollow a Twitter user | `username` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
