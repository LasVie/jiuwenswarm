# Instagram: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `explore` | `public_read` / `low` | `opencli instagram explore [--limit <limit>] -f json`<br>Instagram explore/discover trending posts | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli instagram search "<query>" [--limit <limit>] -f json`<br>Search Instagram users | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `explore`: Source-audited against OpenCLI 1.8.6 instagram/explore.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `search`: Source-audited against OpenCLI 1.8.6 instagram/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
