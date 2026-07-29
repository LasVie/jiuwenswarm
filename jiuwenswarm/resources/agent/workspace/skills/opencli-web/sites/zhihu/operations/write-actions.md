---
opencli_contract:
  version: 2
  site: zhihu
  operation: write-actions
  policy_sha256: 55ef63e4ab56270a7bf67acaaf6364d6ae74c524f167bbcdf0acfa3a33547520
  commands:
    answer:
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
      - help: Zhihu question URL or typed target
        name: target
        positional: true
        required: true
        type: str
      - help: Answer text
        name: text
        positional: true
        required: false
        type: str
      - help: Answer text file path
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

# Zhihu: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `answer` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Answer a Zhihu question | `target` (str, required, positional); `text` (str, optional, positional); `file` (str, optional); `execute` (boolean, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
