# Producthunt: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `browse` | `public_read` / `low` | `opencli producthunt browse "<category>" [--limit <limit>] -f json`<br>Best products in a Product Hunt category | `category` (string, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_intercept; fallback_before=browser_agent; fallback_after=browser_agent |
| `hot` | `public_read` / `low` | `opencli producthunt hot [--limit <limit>] -f json`<br>Today's top Product Hunt launches with vote counts | `limit` (int, optional, default=20) | auth=none; transport=browser_intercept; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `browse`: Source-audited against OpenCLI 1.8.6 producthunt/browse.js; reads public browser-rendered content without authenticated account state.
- `hot`: Source-audited against OpenCLI 1.8.6 producthunt/hot.js; reads public browser-rendered content without authenticated account state.
