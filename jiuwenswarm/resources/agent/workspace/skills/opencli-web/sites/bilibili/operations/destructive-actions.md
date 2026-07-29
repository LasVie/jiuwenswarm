---
opencli_contract:
  version: 2
  site: bilibili
  operation: destructive-actions
  policy_sha256: 6e8e73109dd43108bc96445fe5fb962e20e71bd5fabb4922fa485aa95e9accb6
  commands:
    unfollow:
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
      - help: 目标 UID / 用户名 / space.bilibili.com 链接
        name: target
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

# Bilibili: destructive-actions

Delete, remove, revoke, or perform administrative changes.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `unfollow` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>取消关注 B站用户（官方 API，需登录） | `target` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
