# Bloomberg: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `businessweek` | `public_read` / `low` | `opencli bloomberg businessweek [--limit <limit>] -f json`<br>Bloomberg Businessweek top stories | `limit` (int, optional, default=1) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `crypto` | `public_read` / `low` | `opencli bloomberg crypto [--limit <limit>] -f json`<br>Bloomberg Crypto top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `economics` | `public_read` / `low` | `opencli bloomberg economics [--limit <limit>] -f json`<br>Bloomberg Economics top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `feeds` | `public_read` / `low` | `opencli bloomberg feeds -f json`<br>List the Bloomberg RSS feed aliases used by the adapter | none | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `green` | `public_read` / `low` | `opencli bloomberg green [--limit <limit>] -f json`<br>Bloomberg Green (climate & energy) top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `industries` | `public_read` / `low` | `opencli bloomberg industries [--limit <limit>] -f json`<br>Bloomberg Industries top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `main` | `public_read` / `low` | `opencli bloomberg main [--limit <limit>] -f json`<br>Bloomberg homepage top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `markets` | `public_read` / `low` | `opencli bloomberg markets [--limit <limit>] -f json`<br>Bloomberg Markets top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `opinions` | `public_read` / `low` | `opencli bloomberg opinions [--limit <limit>] -f json`<br>Bloomberg Opinion top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `politics` | `public_read` / `low` | `opencli bloomberg politics [--limit <limit>] -f json`<br>Bloomberg Politics top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `pursuits` | `public_read` / `low` | `opencli bloomberg pursuits [--limit <limit>] -f json`<br>Bloomberg Pursuits (lifestyle) top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `tech` | `public_read` / `low` | `opencli bloomberg tech [--limit <limit>] -f json`<br>Bloomberg Tech top stories (RSS) | `limit` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `businessweek`: Source-audited against OpenCLI 1.8.6 bloomberg/businessweek.js; reads public browser-rendered content without authenticated account state.
