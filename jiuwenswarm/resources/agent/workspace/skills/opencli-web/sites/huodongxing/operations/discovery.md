---
opencli_contract:
  version: 2
  site: huodongxing
  operation: discovery
  policy_sha256: 06399f7a5788f25de4d158035cc75daaa2eb03a1311b3e8e2f3873f2d95232b2
  commands:
    events:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Huodongxing: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `events` | `enabled` | `public_read` / `low` | `opencli_execute(site="huodongxing", operation="discovery", command="events")`<br>活动行活动搜索（按标签、城市、日期、线上/线下、名称过滤） | `tag` (string, optional, default=''); `city` (string, optional, default='全部'); `date` (string, optional, default=''); `dateTo` (string, optional, default=''); `eventType` (int, optional); `qs` (string, optional, default=''); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
