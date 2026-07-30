# Gov Law: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli gov-law search "<query>" [--limit <limit>] -f json`<br>国家法律法规数据库搜索 | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 gov-law/search.js; reads public browser-rendered content without authenticated account state.
