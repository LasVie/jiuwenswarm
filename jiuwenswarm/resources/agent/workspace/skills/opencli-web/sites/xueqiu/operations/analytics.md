---
opencli_contract:
  version: 2
  site: xueqiu
  operation: analytics
  policy_sha256: 7a5406525e083d7bfa2e25b732b8df0543bc33834f5e0471e504ceebe08e0303
  commands:
    earnings-date:
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    kline:
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    stock:
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
      - help: 股票代码，如 SH600519、SZ000858、AAPL、00700
        name: symbol
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Xueqiu: analytics

Read aggregate metrics, trends, or rankings.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `earnings-date` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取股票预计财报发布日期（公司大事） | `symbol` (str, required, positional); `next` (bool, optional, default=False); `limit` (int, optional, default=10) |
| `kline` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取雪球股票K线（历史行情）数据 | `symbol` (str, required, positional); `days` (int, optional, default=14) |
| `stock` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取雪球股票实时行情 | `symbol` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
