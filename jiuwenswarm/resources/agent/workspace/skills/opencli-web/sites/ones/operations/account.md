# Ones: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `me` | `private_account_read` / `medium` | `opencli ones me -f json`<br>ONES Project API — current user (GET users/me) via Chrome Bridge | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `token-info` | `private_account_read` / `medium` | `opencli ones token-info -f json`<br>ONES Project API — session detail (GET auth/token_info) via Chrome Bridge: user, teams, org | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `me`: sensitive output: account identifiers
- `token-info`: sensitive output: account identifiers
