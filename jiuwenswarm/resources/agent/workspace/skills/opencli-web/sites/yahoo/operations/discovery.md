# Yahoo: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli yahoo search "<keyword>" [--limit <limit>] [--page <page>] -f json`<br>Search Yahoo (powered by Bing) | `keyword` (str, required, positional); `limit` (int, optional, default=7); `page` (int, optional, default=1) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 yahoo/search.js; reads public browser-rendered content without authenticated account state.
