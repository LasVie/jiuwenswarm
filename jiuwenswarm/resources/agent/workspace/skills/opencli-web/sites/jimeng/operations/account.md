# Jimeng: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `whoami` | `private_account_read` / `medium` | `opencli jimeng whoami -f json`<br>Show the current logged-in jimeng account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `whoami`: Source-audited against OpenCLI 1.8.6 jimeng/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
