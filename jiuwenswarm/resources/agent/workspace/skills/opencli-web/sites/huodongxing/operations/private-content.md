---
opencli_contract:
  version: 2
  site: huodongxing
  operation: private-content
  policy_sha256: 57ebd108cb1855f944ed0e858466d1c9e219635bd21095a2748d78f40a14bdef
  commands:
    events:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: ''
        help: 活动标签，例如 AI
        name: tag
        required: false
        type: string
      - default: 全部
        help: 城市名，例如 北京 / 上海 / 全部
        name: city
        required: false
        type: string
      - default: ''
        help: 开始日期，格式 YYYY-MM-DD
        name: date
        required: false
        type: string
      - default: ''
        help: 结束日期，格式 YYYY-MM-DD
        name: dateTo
        required: false
        type: string
      - help: 活动类型：1 线下，2 线上
        name: eventType
        required: false
        type: int
      - default: ''
        help: 按活动名称关键词过滤
        name: qs
        required: false
        type: string
      - default: 20
        help: 返回条数（1-50）
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
---

# Huodongxing: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `events` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>活动行活动搜索（按标签、城市、日期、线上/线下、名称过滤） | `tag` (string, optional, default=''); `city` (string, optional, default='全部'); `date` (string, optional, default=''); `dateTo` (string, optional, default=''); `eventType` (int, optional); `qs` (string, optional, default=''); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
