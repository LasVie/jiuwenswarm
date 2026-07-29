---
opencli_contract:
  version: 2
  site: hupu
  operation: discovery
  policy_sha256: 86a3ddfcf16b3fc55407f3ac6dca5cc09098caa7777218d355d2b7e11cea3261
  commands:
    hot:
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
      - default: 20
        help: Number of threads (1-100)
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
    search:
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
      - help: 搜索关键词
        name: query
        positional: true
        required: true
        type: str
      - default: 1
        help: 结果页码
        name: page
        required: false
        type: int
      - default: 20
        help: 返回结果数量
        name: limit
        required: false
        type: int
      - help: 板块ID过滤 (可选)
        name: forum
        required: false
        type: str
      - default: general
        help: '排序方式: general/createtime/replytime/light/reply'
        name: sort
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Hupu: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="hupu", operation="discovery", command="hot")`<br>虎扑首页热门帖子（含 lights / replies / forum / is_hot 列） | `limit` (int, optional, default=20) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="hupu", operation="discovery", command="search", arguments={"query":"<query>"})`<br>搜索虎扑帖子 (使用官方API) | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20); `forum` (str, optional); `sort` (str, optional, default='general') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
