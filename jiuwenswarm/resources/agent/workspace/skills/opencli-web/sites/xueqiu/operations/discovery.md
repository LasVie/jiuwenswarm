---
opencli_contract:
  version: 2
  site: xueqiu
  operation: discovery
  policy_sha256: 7a5406525e083d7bfa2e25b732b8df0543bc33834f5e0471e504ceebe08e0303
  commands:
    hot:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: 返回数量，默认 20，最大 50
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    hot-stock:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: 返回数量，默认 20，最大 50
        name: limit
        required: false
        type: int
      - default: '10'
        help: 榜单类型 10=人气榜(默认) 12=关注榜
        name: type
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 搜索关键词，如 茅台、AAPL、腾讯
        name: query
        positional: true
        required: true
        type: str
      - default: 10
        help: 返回数量，默认 10
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Xueqiu: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hot` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取雪球热门动态 | `limit` (int, optional, default=20) |
| `hot-stock` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取雪球热门股票榜 | `limit` (int, optional, default=20); `type` (str, optional, default='10') |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>搜索雪球股票（代码或名称） | `query` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
