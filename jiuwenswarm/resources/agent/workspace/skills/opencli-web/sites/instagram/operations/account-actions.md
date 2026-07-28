---
opencli_contract:
  version: 2
  site: instagram
  operation: account-actions
  policy_sha256: d42c25c598970ce1716e696af43fd6eb6c2acc1199441ba3a3b95731834e32ef
  commands:
    follow:
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
      - help: Instagram username to follow
        name: username
        positional: true
        required: true
        type: str
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
    save:
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

# Instagram: account-actions

Change reversible account relationship or saved state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `follow` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Follow an Instagram user | `username` (str, required, positional) |
| `like` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Like an Instagram post | `username` (str, required, positional); `index` (int, optional, default=1) |
| `save` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Save (bookmark) an Instagram post | `username` (str, required, positional); `index` (int, optional, default=1) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
