# Suno: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `status` | `private_account_read` / `medium` | `opencli suno status -f json`<br>Check Suno login, plan, credit balance, and captcha readiness | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli suno whoami -f json`<br>Show the current logged-in suno account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `status`: sensitive output: account identifiers
- `whoami`: sensitive output: account identifiers
