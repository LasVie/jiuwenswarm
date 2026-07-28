---
opencli_contract:
  version: 2
  site: zhihu
  operation: account-actions
  policy_sha256: 72cfde1a8e42b9be48a1414fe1c119c65782c8b4c07c241be09bd6fcad8a4929
  commands:
    favorite:
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
      - help: Zhihu target URL or typed target
        name: target
        positional: true
        required: true
        type: str
      - help: Collection name
        name: collection
        required: false
        type: str
      - help: Stable collection id
        name: collection-id
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
      - help: Zhihu target URL or typed target
        name: target
        positional: true
        required: true
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
      - help: Zhihu target URL or typed target
        name: target
        positional: true
        required: true
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

# Zhihu: account-actions

Change reversible account relationship or saved state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `favorite` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Favorite a Zhihu answer or article into a specific collection | `target` (str, required, positional); `collection` (str, optional); `collection-id` (str, optional); `execute` (boolean, optional) |
| `follow` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Follow a Zhihu user or question | `target` (str, required, positional); `execute` (boolean, optional) |
| `like` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Like a Zhihu answer or article | `target` (str, required, positional); `execute` (boolean, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
