---
opencli_contract:
  version: 2
  site: douban
  operation: private-content
  policy_sha256: d2fadddfa14cdb365fea4b172c4ce959c5c5179f435b303b359a5dcb000337d7
  commands:
    marks:
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
      - choices:
        - collect
        - wish
        - do
        - all
        default: collect
        help: '标记类型: collect(看过), wish(想看), do(在看), all(全部)'
        name: status
        required: false
        type: str
      - default: 50
        help: 导出数量， 0 表示全部
        name: limit
        required: false
        type: int
      - help: 用户ID，不填则使用当前登录账号
        name: uid
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    reviews:
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
      - default: 20
        help: 导出数量
        name: limit
        required: false
        type: int
      - help: 用户ID，不填则使用当前登录账号
        name: uid
        required: false
        type: str
      - default: false
        help: 获取完整影评内容
        name: full
        required: false
        type: bool
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

# Douban: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `marks` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>导出个人观影标记 | `status` (str, optional, default='collect', choices=collect,wish,do,all); `limit` (int, optional, default=50); `uid` (str, optional) |
| `reviews` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>导出个人影评 | `limit` (int, optional, default=20); `uid` (str, optional); `full` (bool, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
