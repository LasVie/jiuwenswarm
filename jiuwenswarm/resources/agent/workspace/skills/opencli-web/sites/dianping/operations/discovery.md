# Dianping: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli dianping search "<keyword>" [--city "<city>"] [--limit <limit>] -f json`<br>大众点评店铺搜索（按关键词 + 城市） | `keyword` (str, required, positional); `city` (str, optional); `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 dianping/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
