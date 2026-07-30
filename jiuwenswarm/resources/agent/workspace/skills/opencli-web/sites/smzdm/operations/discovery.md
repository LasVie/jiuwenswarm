# Smzdm: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli smzdm search "<query>" [--limit <limit>] -f json`<br>什么值得买搜索好价 | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 smzdm/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
