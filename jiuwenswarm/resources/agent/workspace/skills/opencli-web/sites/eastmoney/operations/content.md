---
opencli_contract:
  version: 2
  site: eastmoney
  operation: content
  policy_sha256: b7f30feb341de0d9feaa6dc7aae0a3f572a5e5f815f50f33de746cba12334a0e
  commands:
    announcement:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: SHA,SZA,BJA
        help: 交易所：SHA (沪) / SZA (深) / BJA (北) 可逗号分隔
        name: market
        required: false
        type: string
      - default: 20
        help: 返回数量 (max 100)
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
    convertible:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: turnover
        help: 排序：turnover / change / drop / price / premium
        name: sort
        required: false
        type: string
      - default: 20
        help: 返回数量 (max 100)
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
    etf:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: turnover
        help: 排序：turnover / change / drop / volume / rate
        name: sort
        required: false
        type: string
      - default: 20
        help: 返回数量 (max 100)
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
    holders:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: A股代码（600519 / sh600519 等）
        name: symbol
        positional: true
        required: true
        type: str
      - default: 10
        help: 返回股东数（默认十大流通股东）
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
    index-board:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: main
        help: 指数分组：main (A股主要), hk (港股), us (美股), all
        name: group
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    kline:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: 股票代码（A/HK/US 均可）
        name: symbol
        positional: true
        required: true
        type: str
      - default: day
        help: 周期：1m/5m/15m/30m/60m/day/week/month
        name: period
        required: false
        type: string
      - default: forward
        help: 复权：none / forward / backward
        name: adjust
        required: false
        type: string
      - default: 30
        help: 返回最近 N 根（末尾）
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
    kuaixun:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: '102'
        help: 频道：102 (重要) / 101 (全部) / 104 / 105 / 106 / 107
        name: column
        required: false
        type: string
      - default: 20
        help: 返回数量 (max 100)
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
    longhu:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: ''
        help: 开始交易日 YYYY-MM-DD (默认昨天)
        name: date
        required: false
        type: string
      - default: 20
        help: 返回数量 (max 100)
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
    money-flow:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: today
        help: 周期：today / 5d / 10d
        name: range
        required: false
        type: string
      - default: desc
        help: 排序：desc (净流入排行) / asc (净流出)
        name: order
        required: false
        type: string
      - default: 20
        help: 返回数量 (max 100)
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
    northbound:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: north
        help: 方向：north (北向，即外资买A) / south (南向，即内地买港)
        name: direction
        required: false
        type: string
      - default: 10
        help: 返回最近 N 分钟
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
    quote:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: 股票代码（可用逗号/空格分隔多个）
        name: symbols
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    rank:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: hs-a
        help: 市场：hs-a / sh-a / sz-a / bj-a / cyb / kcb / hk / us
        name: market
        required: false
        type: string
      - default: change
        help: 排序：change / drop / turnover / volume / amplitude / rate
        name: sort
        required: false
        type: string
      - default: 20
        help: 返回数量 (max 100)
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
    sectors:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: industry
        help: 板块类型：industry / concept / region
        name: type
        required: false
        type: string
      - default: change
        help: 排序：change / drop / money-flow / out-flow / turnover
        name: sort
        required: false
        type: string
      - default: 20
        help: 返回数量 (max 100)
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

# Eastmoney: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `announcement` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="announcement")`<br>上市公司公告（按交易所筛选） | `market` (string, optional, default='SHA,SZA,BJA'); `limit` (int, optional, default=20) |
| `convertible` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="convertible")`<br>可转债行情列表（默认按成交额排序） | `sort` (string, optional, default='turnover'); `limit` (int, optional, default=20) |
| `etf` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="etf")`<br>ETF 列表按成交额/涨跌幅排行 | `sort` (string, optional, default='turnover'); `limit` (int, optional, default=20) |
| `holders` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="holders", arguments={"symbol":"<symbol>"})`<br>十大流通股东（A股 F10 数据） | `symbol` (str, required, positional); `limit` (int, optional, default=10) |
| `index-board` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="index-board")`<br>主要市场指数行情（A股 / 港股 / 美股） | `group` (string, optional, default='main') |
| `kline` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="kline", arguments={"symbol":"<symbol>"})`<br>K线历史数据（分/日/周/月/前复权/后复权） | `symbol` (str, required, positional); `period` (string, optional, default='day'); `adjust` (string, optional, default='forward'); `limit` (int, optional, default=30) |
| `kuaixun` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="kuaixun")`<br>东方财富 7x24 财经快讯 | `column` (string, optional, default='102'); `limit` (int, optional, default=20) |
| `longhu` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="longhu")`<br>龙虎榜明细（A股交易所公开披露榜单） | `date` (string, optional, default=''); `limit` (int, optional, default=20) |
| `money-flow` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="money-flow")`<br>主力资金净流入排行（今日/5日/10日） | `range` (string, optional, default='today'); `order` (string, optional, default='desc'); `limit` (int, optional, default=20) |
| `northbound` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="northbound")`<br>沪深港通北向/南向资金当日分时净流入（万元） | `direction` (string, optional, default='north'); `limit` (int, optional, default=10) |
| `quote` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="quote", arguments={"symbols":"<symbols>"})`<br>个股实时行情（A股 / 港股 / 美股）— 来自 push2.eastmoney.com | `symbols` (str, required, positional) |
| `rank` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="rank")`<br>东财市场涨跌/成交排行（沪深/北证/创/科/港/美） | `market` (string, optional, default='hs-a'); `sort` (string, optional, default='change'); `limit` (int, optional, default=20) |
| `sectors` | `enabled` | `public_read` / `low` | `opencli_execute(site="eastmoney", operation="content", command="sectors")`<br>板块排行（行业/概念/地域）按涨跌幅、主力资金或成交额排序 | `type` (string, optional, default='industry'); `sort` (string, optional, default='change'); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
