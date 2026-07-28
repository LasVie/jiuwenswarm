---
opencli_contract:
  version: 2
  site: twitter
  operation: account-actions
  policy_sha256: d3dfdd9f50e334a4672153f072546b8d93fc2b4c68dc2786edab05aea347b96c
  commands:
    bookmark:
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
      - help: Tweet URL to bookmark
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
    follow:
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
    follow-batch:
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
      - help: Comma-separated Twitter/X screen names, with or without @
        name: usernames
        positional: true
        required: true
        type: string
      - default: 3000
        help: Delay between follow attempts in milliseconds
        name: delay-ms
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    like:
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
      - help: The URL of the tweet to like
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

# Twitter: account-actions

Change reversible account relationship or saved state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `bookmark` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Bookmark a tweet | `url` (string, required, positional) |
| `follow` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Follow a Twitter user | `username` (string, required, positional) |
| `follow-batch` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Follow multiple Twitter/X users from a comma-separated username list | `usernames` (string, required, positional); `delay-ms` (int, optional, default=3000) |
| `like` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Like a specific tweet | `url` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
