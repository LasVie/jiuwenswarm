# Xianyu: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `whoami` | `private_account_read` / `medium` | `opencli xianyu whoami -f json`<br>Show the current logged-in xianyu account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `whoami`: sensitive output: account identifiers
