# Indeed: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli indeed search "<query>" [--location "<location>"] [--fromage "<fromage>"] [--sort "<sort>"] [--start <start>] [--limit <limit>] -f json`<br>Indeed keyword job search (rendered DOM via browser session, US site) | `query` (str, required, positional); `location` (string, optional, default=''); `fromage` (string, optional, default=''); `sort` (string, optional, default='relevance'); `start` (int, optional, default=0); `limit` (int, optional, default=15) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 indeed/search.js; reads public browser-rendered content without authenticated account state.
