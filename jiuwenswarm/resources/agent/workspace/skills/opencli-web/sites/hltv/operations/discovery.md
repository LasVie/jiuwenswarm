# Hltv: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli hltv search "<query>" [--limit <limit>] -f json`<br>Search HLTV players, teams, events, and articles | `query` (string, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 hltv/search.js; reads public browser-rendered content without authenticated account state.
