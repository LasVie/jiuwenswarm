---
opencli_contract:
  version: 2
  site: 1point3acres
  operation: private-content
  policy_sha256: 0dbf244c9dd700c1aecb310892b943018ea6fe2ca7e725c441382de5c8b20b26
  commands:
    notifications:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: mypost
        help: 通知类型：mypost（我的帖子） / interactive（互动） / system（系统） / app（应用）
        name: kind
        required: false
        type: string
      - default: 20
        help: 返回条数
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    search:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 搜索关键字
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: 返回条数（默认 20，最多 50）
        name: limit
        required: false
        type: int
      - default: ''
        help: 限定版块 ID（可选）
        name: fid
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# 1Point3Acres: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `notifications` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>一亩三分地 站内通知（互动 / 点评 / @ 我；需要登录） | `kind` (string, optional, default='mypost'); `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>一亩三分地 站内关键字搜索（需要登录） | `query` (str, required, positional); `limit` (int, optional, default=20); `fid` (string, optional, default='') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
