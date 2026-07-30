# Tieba: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli tieba hot [--limit <limit>] -f json`<br>Tieba hot topics | `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `posts` | `public_read` / `low` | `opencli tieba posts "<forum>" [--page <page>] [--limit <limit>] -f json`<br>Browse posts in a tieba forum | `forum` (string, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli tieba search "<keyword>" [--page <1>] [--limit <limit>] -f json`<br>Search posts across tieba | `keyword` (string, required, positional); `page` (int, optional, default=1, choices=1); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `hot`: Source-audited against OpenCLI 1.8.6 tieba/hot.js; reads public browser-rendered content without authenticated account state.
- `posts`: Source-audited against OpenCLI 1.8.6 tieba/posts.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `search`: Source-audited against OpenCLI 1.8.6 tieba/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
