# Xiaohongshu: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `login` | `auth_session_change` / `high` | `opencli xiaohongshu login [--timeout <timeout>] -f json`<br>Open xiaohongshu login and wait until the browser session is authenticated | `timeout` (int, optional, default=300) | auth=interactive; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli xiaohongshu whoami -f json`<br>Show the current logged-in xiaohongshu account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `whoami`: sensitive output: account identifiers
