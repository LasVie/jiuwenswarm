---
opencli_contract:
  version: 2
  site: xueqiu
  operation: account
  policy_sha256: 7a5406525e083d7bfa2e25b732b8df0543bc33834f5e0471e504ceebe08e0303
  commands:
    fund-holdings:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: high
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
      - financial account data
      - account identifiers
    fund-snapshot:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
      risk: high
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
      - financial account data
      - account identifiers
    groups:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
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
      - private portfolio data
      - account identifiers
    watchlist:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
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
      - private portfolio data
      - account identifiers
    whoami:
      executor: none
      execution_state: disabled
      semantic_effect: private_account_read
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
      - account identifiers
---

# Xueqiu: account

Read account identity or account-scoped metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `fund-holdings` | `disabled` | `private_account_read` / `high` | Not executable; use the declared fallback if permitted<br>获取蛋卷基金持仓明细（可用 --account 按子账户过滤） | `account` (str, optional, default='') |
| `fund-snapshot` | `disabled` | `private_account_read` / `high` | Not executable; use the declared fallback if permitted<br>获取蛋卷基金快照（总资产、子账户、持仓，推荐 -f json 输出） | none |
| `groups` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球自选股分组列表（含模拟组合） | none |
| `watchlist` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取雪球自选股/模拟组合股票列表 | `pid` (str, optional, default='-1'); `limit` (int, optional, default=100) |
| `whoami` | `disabled` | `private_account_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show the current logged-in xueqiu account | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
