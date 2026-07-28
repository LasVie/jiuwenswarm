---
opencli_contract:
  version: 2
  site: jike
  operation: write-actions
  policy_sha256: f05c6947bf8b738be4ec401e0cae980808f3b984f8d6143c3bf0e4ac951e3323
  commands:
    repost:
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
      - help: 帖子 ID
        name: id
        positional: true
        required: true
        type: string
      - help: 转发附言（可选）
        name: text
        positional: true
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Jike: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `repost` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>转发即刻帖子 | `id` (string, required, positional); `text` (string, optional, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
