---
opencli_contract:
  version: 2
  site: instagram
  operation: write-actions
  policy_sha256: d42c25c598970ce1716e696af43fd6eb6c2acc1199441ba3a3b95731834e32ef
  commands:
    note:
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
      - help: Note text (max 60 characters)
        name: content
        positional: true
        required: true
        type: str
      - default: 120
        help: 'Max seconds for the overall command (default: 120)'
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
    reel:
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
      - help: Path to a single .mp4 video file
        name: video
        required: false
        type: str
        valueRequired: true
      - help: Caption text
        name: content
        positional: true
        required: false
        type: str
      - default: 600
        help: 'Max seconds for the overall command (default: 600)'
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
    story:
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
      - help: Path to a single story image or video file
        name: media
        required: false
        type: str
        valueRequired: true
      - default: 300
        help: 'Max seconds for the overall command (default: 300)'
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
    unlike:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Username of the post author
        name: username
        positional: true
        required: true
        type: str
      - default: 1
        help: Post index (1 = most recent)
        name: index
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    unsave:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Username of the post author
        name: username
        positional: true
        required: true
        type: str
      - default: 1
        help: Post index (1 = most recent)
        name: index
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

# Instagram: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `note` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Publish a text Instagram note | `content` (str, required, positional); `timeout` (int, optional, default=120) |
| `reel` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Post an Instagram reel video | `video` (str, optional); `content` (str, optional, positional); `timeout` (int, optional, default=600) |
| `story` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Post a single Instagram story image or video | `media` (str, optional); `timeout` (int, optional, default=300) |
| `unlike` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Unlike an Instagram post | `username` (str, required, positional); `index` (int, optional, default=1) |
| `unsave` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Unsave (remove bookmark) an Instagram post | `username` (str, required, positional); `index` (int, optional, default=1) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
