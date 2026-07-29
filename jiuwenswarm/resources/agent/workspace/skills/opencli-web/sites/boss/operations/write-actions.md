---
opencli_contract:
  version: 2
  site: boss
  operation: write-actions
  policy_sha256: 0512851bb10f8f329773a56b353cc02733b09e02ba73228f57eeb2307bd963c3
  commands:
    batchgreet:
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
      - default: ''
        help: Filter by encrypted job ID (greet all jobs if empty)
        name: job-id
        required: false
        type: str
      - default: 5
        help: Max candidates to greet
        name: limit
        required: false
        type: int
      - default: ''
        help: Custom greeting message (uses default if empty)
        name: text
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    exchange:
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
      - help: Encrypted UID of the candidate
        name: uid
        positional: true
        required: true
        type: str
      - choices:
        - phone
        - wechat
        default: phone
        help: 'Exchange type: phone or wechat'
        name: type
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    greet:
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
      - help: Encrypted UID of the candidate (from recommend)
        name: uid
        positional: true
        required: true
        type: str
      - help: Security ID of the candidate
        name: security-id
        required: true
        type: str
      - help: Encrypted job ID
        name: job-id
        required: true
        type: str
      - default: ''
        help: Custom greeting message (uses default template if empty)
        name: text
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    mark:
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
      - help: Encrypted UID of the candidate
        name: uid
        positional: true
        required: true
        type: str
      - help: Label name (新招呼/沟通中/已约面/已获取简历/已交换电话/已交换微信/不合适/收藏) or label ID
        name: label
        required: true
        type: str
      - default: false
        help: Remove the label instead of adding
        name: remove
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

# Boss: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `batchgreet` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>BOSS直聘批量向推荐候选人发送招呼 | `job-id` (str, optional, default=''); `limit` (int, optional, default=5); `text` (str, optional, default='') |
| `exchange` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>BOSS直聘交换联系方式（请求手机/微信） | `uid` (str, required, positional); `type` (str, optional, default='phone', choices=phone,wechat) |
| `greet` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>BOSS直聘向新候选人发送招呼（开始聊天） | `uid` (str, required, positional); `security-id` (str, required); `job-id` (str, required); `text` (str, optional, default='') |
| `mark` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>BOSS直聘给候选人添加标签 | `uid` (str, required, positional); `label` (str, required); `remove` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
