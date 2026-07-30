# Xueqiu: analytics

Read aggregate metrics, trends, or rankings.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `earnings-date` | `public_read` / `low` | `opencli xueqiu earnings-date "<symbol>" [--next <true\|false>] [--limit <limit>] -f json`<br>获取股票预计财报发布日期（公司大事） | `symbol` (str, required, positional); `next` (bool, optional, default=False); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `kline` | `public_read` / `low` | `opencli xueqiu kline "<symbol>" [--days <days>] -f json`<br>获取雪球股票K线（历史行情）数据 | `symbol` (str, required, positional); `days` (int, optional, default=14) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `stock` | `public_read` / `low` | `opencli xueqiu stock "<symbol>" -f json`<br>获取雪球股票实时行情 | `symbol` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `earnings-date`: Source-audited against OpenCLI 1.8.6 xueqiu/earnings-date.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `kline`: Source-audited against OpenCLI 1.8.6 xueqiu/kline.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `stock`: Source-audited against OpenCLI 1.8.6 xueqiu/stock.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
