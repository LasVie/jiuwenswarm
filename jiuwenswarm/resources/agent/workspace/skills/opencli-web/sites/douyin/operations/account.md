# Douyin: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `profile` | `private_account_read` / `medium` | `opencli douyin profile -f json`<br>获取账号信息 | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli douyin whoami -f json`<br>Show the current logged-in douyin account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `profile`: sensitive output: account identifiers
- `whoami`: sensitive output: account identifiers
