# Jianyu: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli jianyu search "<query>" [--limit <limit>] [--since_days <since_days>] -f json`<br>搜索剑鱼标讯公告 | `query` (str, required, positional); `limit` (int, optional, default=20); `since_days` (int, optional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 jianyu/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
