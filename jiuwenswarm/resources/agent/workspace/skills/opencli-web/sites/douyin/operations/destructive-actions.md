---
opencli_contract:
  version: 2
  site: douyin
  operation: destructive-actions
  policy_sha256: 44a88f4e2945603337450f4d82e1d94d30556064265afb43719f582edd8ebf4c
  commands:
    delete:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 作品 ID / item_id
        name: aweme_id
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
---

# Douyin: destructive-actions

Delete, remove, revoke, or perform administrative changes.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `delete` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>删除作品（优先使用创作者后台作品管理；找不到时回退到旧删除接口） | `aweme_id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
