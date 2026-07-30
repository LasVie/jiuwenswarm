# Gov Law: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `recent` | `public_read` / `low` | `opencli gov-law recent [--limit <limit>] -f json`<br>最新法律法规 | `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `recent`: Source-audited against OpenCLI 1.8.6 gov-law/recent.js; reads public browser-rendered content without authenticated account state.
