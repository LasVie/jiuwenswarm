# Nowcoder: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli nowcoder search "<query>" [--type "<type>"] [--limit <limit>] -f json`<br>Full-text search | `query` (str, required, positional); `type` (str, optional, default='all'); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `suggest` | `public_read` / `low` | `opencli nowcoder suggest "<query>" -f json`<br>Search suggestions | `query` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `trending` | `public_read` / `low` | `opencli nowcoder trending [--limit <limit>] -f json`<br>Trending posts | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 nowcoder/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `suggest`: Source-audited against OpenCLI 1.8.6 nowcoder/suggest.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
