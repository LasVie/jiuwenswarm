# Upwork: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `public_read` / `low` | `opencli upwork detail "<id>" -f json`<br>Read the full Upwork job posting by ciphertext id (e.g. ~022054964136512093518) | `id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 upwork/detail.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
