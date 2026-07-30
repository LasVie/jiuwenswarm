# Tiktok: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `explore` | `public_read` / `low` | `opencli tiktok explore [--limit <limit>] -f json`<br>Get trending TikTok videos from the recommend feed via page-context APIs | `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `live` | `public_read` / `low` | `opencli tiktok live [--limit <limit>] -f json`<br>Browse TikTok live streams via page-context APIs | `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli tiktok search "<query>" [--limit <limit>] -f json`<br>Search TikTok videos | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `explore`: Source-audited against OpenCLI 1.8.6 tiktok/explore.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `live`: Source-audited against OpenCLI 1.8.6 tiktok/live.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `search`: Source-audited against OpenCLI 1.8.6 tiktok/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
