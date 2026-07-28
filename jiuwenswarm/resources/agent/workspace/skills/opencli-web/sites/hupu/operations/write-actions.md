---
opencli_contract:
  version: 2
  site: hupu
  operation: write-actions
  policy_sha256: 292f24b86db7d4f26303e6f4a06f0f3d1645ab8dd5f083536c37d5c5d2acee73
  commands:
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
      - help: 帖子ID（9位数字）
        name: tid
        positional: true
        required: true
        type: str
      - help: 回复ID
        name: pid
        positional: true
        required: true
        type: str
      - help: 板块ID（如278汽车区）
        name: fid
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

# Hupu: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `unlike` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>取消点赞虎扑回复 (需要登录) | `tid` (str, required, positional); `pid` (str, required, positional); `fid` (str, required) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
