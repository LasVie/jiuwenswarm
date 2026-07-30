# Brave: web-search

Read browser-rendered web search results.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli brave search "<keyword>" [--limit <limit>] [--offset <offset>] -f json`<br>Search Brave Search | `keyword` (str, required, positional); `limit` (int, optional, default=10); `offset` (int, optional, default=0) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 brave/search.js; reads public browser-rendered content without authenticated account state.
