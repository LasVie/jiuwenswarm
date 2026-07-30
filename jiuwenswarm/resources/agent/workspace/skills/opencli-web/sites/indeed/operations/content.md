# Indeed: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `job` | `public_read` / `low` | `opencli indeed job "<id>" -f json`<br>Read the full Indeed job posting by jk (job key) | `id` (str, required, positional) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `job`: Source-audited against OpenCLI 1.8.6 indeed/job.js; reads public browser-rendered content without authenticated account state.
