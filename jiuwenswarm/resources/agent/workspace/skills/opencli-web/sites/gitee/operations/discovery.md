# Gitee: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli gitee search "<keyword>" [--limit <limit>] -f json`<br>Search repositories on Gitee | `keyword` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `trending` | `public_read` / `low` | `opencli gitee trending [--limit <limit>] -f json`<br>Recommended open-source projects on Gitee Explore | `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 gitee/search.js; reads public browser-rendered content without authenticated account state.
- `trending`: Source-audited against OpenCLI 1.8.6 gitee/trending.js; reads public browser-rendered content without authenticated account state.
