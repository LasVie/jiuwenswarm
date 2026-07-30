# Xueqiu: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli xueqiu hot [--limit <limit>] -f json`<br>获取雪球热门动态 | `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `hot-stock` | `public_read` / `low` | `opencli xueqiu hot-stock [--limit <limit>] [--type "<type>"] -f json`<br>获取雪球热门股票榜 | `limit` (int, optional, default=20); `type` (str, optional, default='10') | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli xueqiu search "<query>" [--limit <limit>] -f json`<br>搜索雪球股票（代码或名称） | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `hot`: Source-audited against OpenCLI 1.8.6 xueqiu/hot.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `hot-stock`: Source-audited against OpenCLI 1.8.6 xueqiu/hot-stock.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `search`: Source-audited against OpenCLI 1.8.6 xueqiu/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
