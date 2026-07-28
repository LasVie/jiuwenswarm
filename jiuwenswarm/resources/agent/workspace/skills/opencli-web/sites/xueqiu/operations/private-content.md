---
opencli_contract:
  version: 2
  site: xueqiu
  operation: private-content
  policy_sha256: 28a80b6191b319627b7263b284950f471ad7737411dbe798e70f0e89ae28630b
  commands:
    comments:
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
      - help: Stock symbol, e.g. SH600519, AAPL, or 00700
        name: symbol
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of discussion posts to return
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
    earnings-date:
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
      - help: 股票代码，如 SH600519、SZ000858、00700
        name: symbol
        positional: true
        required: true
        type: str
      - default: false
        help: 仅返回最近一次未发布的财报日期
        name: next
        required: false
        type: bool
      - default: 10
        help: 返回数量，默认 10
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
    feed:
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
      - default: 1
        help: 页码，默认 1
        name: page
        required: false
        type: int
      - default: 20
        help: 每页数量，默认 20
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
    fund-holdings:
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
      - default: ''
        help: 按子账户名称或 ID 过滤
        name: account
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
    fund-snapshot:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    groups:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    hot:
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
        help: 返回数量，默认 20，最大 50
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
    hot-stock:
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    kline:
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
      - help: 股票代码，如 SH600519、SZ000858、AAPL
        name: symbol
        positional: true
        required: true
        type: str
      - default: 14
        help: 回溯天数（默认14天）
        name: days
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    stock:
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
      - help: 股票代码，如 SH600519、SZ000858、AAPL、00700
        name: symbol
        positional: true
        required: true
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
    watchlist:
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
      - default: '-1'
        help: 分组ID：-1=全部(默认) -4=模拟 -5=沪深 -6=美股 -7=港股 -10=实盘 0=持仓（通过 xueqiu groups 获取）
        name: pid
        required: false
        type: str
      - default: 100
        help: 默认 100
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

# Xueqiu: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comments` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取单只股票的讨论动态 | `symbol` (str, required, positional); `limit` (int, optional, default=20) |
| `earnings-date` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取股票预计财报发布日期（公司大事） | `symbol` (str, required, positional); `next` (bool, optional, default=False); `limit` (int, optional, default=10) |
| `feed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球首页时间线（关注用户的动态） | `page` (int, optional, default=1); `limit` (int, optional, default=20) |
| `fund-holdings` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取蛋卷基金持仓明细（可用 --account 按子账户过滤） | `account` (str, optional, default='') |
| `fund-snapshot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取蛋卷基金快照（总资产、子账户、持仓，推荐 -f json 输出） | none |
| `groups` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球自选股分组列表（含模拟组合） | none |
| `hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球热门动态 | `limit` (int, optional, default=20) |
| `hot-stock` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球热门股票榜 | `limit` (int, optional, default=20); `type` (str, optional, default='10') |
| `kline` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球股票K线（历史行情）数据 | `symbol` (str, required, positional); `days` (int, optional, default=14) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>搜索雪球股票（代码或名称） | `query` (str, required, positional); `limit` (int, optional, default=10) |
| `stock` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球股票实时行情 | `symbol` (str, required, positional) |
| `watchlist` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球自选股/模拟组合股票列表 | `pid` (str, optional, default='-1'); `limit` (int, optional, default=100) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
