# V2Ex: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `me` | `private_account_read` / `medium` | `opencli v2ex me -f json`<br>V2EX 获取个人资料 (余额/未读提醒) | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli v2ex whoami -f json`<br>Show the current logged-in v2ex account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `me`: Source-audited against OpenCLI 1.8.6 v2ex/me.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers, account balance
- `whoami`: Source-audited against OpenCLI 1.8.6 v2ex/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
