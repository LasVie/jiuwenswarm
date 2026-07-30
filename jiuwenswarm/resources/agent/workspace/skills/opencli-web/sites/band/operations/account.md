# Band: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `bands` | `private_account_read` / `medium` | `opencli band bands -f json`<br>List all Bands you belong to | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli band whoami -f json`<br>Show the current logged-in band account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `bands`: Source-audited against OpenCLI 1.8.6 band/bands.js; reads current browser-session or account-scoped metadata.; sensitive output: group memberships, account identifiers
- `whoami`: Source-audited against OpenCLI 1.8.6 band/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
