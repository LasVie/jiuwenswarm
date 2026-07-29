---
opencli_contract:
  version: 2
  site: xianyu
  operation: discovery
  policy_sha256: 0b1f86865cbb71357073bb7e393c4e3269c06a66493a4eca1d0c53b4c0912bca
  commands:
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 搜索关键词
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: 返回结果数（最多 60，自动翻页）
        name: limit
        required: false
        type: int
      - help: 最低价格（元），服务端筛选
        name: min-price
        required: false
        type: float
      - help: 最高价格（元），服务端筛选
        name: max-price
        required: false
        type: float
      - help: 省份名（如 广东），服务端按地区筛选
        name: province
        required: false
        type: string
      - help: 城市名（如 深圳 / 湛江），可单独使用，服务端按地区筛选
        name: city
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Xianyu: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>搜索闲鱼商品（支持服务端价格区间 / 地区筛选） | `query` (str, required, positional); `limit` (int, optional, default=20); `min-price` (float, optional); `max-price` (float, optional); `province` (string, optional); `city` (string, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
