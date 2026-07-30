# 12306: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `me` | `private_account_read` / `medium` | `opencli 12306 me [--include-sensitive <true\|false>] -f json`<br>Show the logged-in 12306 account summary. Sensitive fields (real name, email, mobile, birth date) are masked by default; pass --include-sensitive to opt in. | `include-sensitive` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli 12306 whoami -f json`<br>Show the current logged-in 12306 account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `me`: sensitive output: account identifiers
- `whoami`: sensitive output: account identifiers
