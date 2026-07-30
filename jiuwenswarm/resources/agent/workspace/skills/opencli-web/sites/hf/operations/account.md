# Hf: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `whoami` | `private_account_read` / `medium` | `opencli hf whoami -f json`<br>Show the current logged-in hf account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `whoami`: Source-audited against OpenCLI 1.8.6 hf/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
