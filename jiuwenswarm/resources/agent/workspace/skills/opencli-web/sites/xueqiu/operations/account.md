# Xueqiu: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `fund-holdings` | `private_account_read` / `high` | `opencli xueqiu fund-holdings [--account "<account>"] -f json`<br>获取蛋卷基金持仓明细（可用 --account 按子账户过滤） | `account` (str, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `fund-snapshot` | `private_account_read` / `high` | `opencli xueqiu fund-snapshot -f json`<br>获取蛋卷基金快照（总资产、子账户、持仓，推荐 -f json 输出） | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `groups` | `private_account_read` / `medium` | `opencli xueqiu groups -f json`<br>获取雪球自选股分组列表（含模拟组合） | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `watchlist` | `private_account_read` / `medium` | `opencli xueqiu watchlist [--pid "<pid>"] [--limit <limit>] -f json`<br>获取雪球自选股/模拟组合股票列表 | `pid` (str, optional, default='-1'); `limit` (int, optional, default=100) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli xueqiu whoami -f json`<br>Show the current logged-in xueqiu account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `fund-holdings`: Source-audited against OpenCLI 1.8.6 xueqiu/fund-holdings.js; reads current browser-session or account-scoped metadata.; sensitive output: financial account data, account identifiers
- `fund-snapshot`: Source-audited against OpenCLI 1.8.6 xueqiu/fund-snapshot.js; reads current browser-session or account-scoped metadata.; sensitive output: financial account data, account identifiers
- `groups`: Source-audited against OpenCLI 1.8.6 xueqiu/groups.js; reads current browser-session or account-scoped metadata.; sensitive output: private portfolio data, account identifiers
- `watchlist`: Source-audited against OpenCLI 1.8.6 xueqiu/watchlist.js; reads current browser-session or account-scoped metadata.; sensitive output: private portfolio data, account identifiers
- `whoami`: Source-audited against OpenCLI 1.8.6 xueqiu/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
