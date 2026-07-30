# Bilibili: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `me` | `private_account_read` / `medium` | `opencli bilibili me -f json`<br>My Bilibili profile info | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli bilibili whoami -f json`<br>Show the current logged-in bilibili account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `me`: sensitive output: account identifiers
- `whoami`: sensitive output: account identifiers
