---
opencli_contract:
  version: 2
  site: bilibili
  operation: account-actions
  policy_sha256: 79262d9ab33f66ec264abde1f4e74f443b2285e92443fd0272d5197bfc948436
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
      - help: Favorite folder ID (defaults to first folder)
        name: fid
        required: false
        type: int
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
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

# Bilibili: account-actions

Change reversible account relationship or saved state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `favorite` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>我的收藏夹 | `fid` (int, optional); `limit` (int, optional, default=20); `page` (int, optional, default=1) |
| `follow` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>关注 B站用户（官方 API，需登录） | `target` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
