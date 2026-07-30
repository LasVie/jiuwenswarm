# Coupang: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli coupang search "<query>" [--page <page>] [--limit <limit>] [--filter "<filter>"] -f json`<br>Search Coupang products with logged-in browser session | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20); `filter` (str, optional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 coupang/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
