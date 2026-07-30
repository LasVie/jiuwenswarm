# Weibo: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `me` | `private_account_read` / `medium` | `opencli weibo me -f json`<br>My Weibo profile info | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli weibo whoami -f json`<br>Show the current logged-in weibo account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `me`: Source-audited against OpenCLI 1.8.6 weibo/me.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
- `whoami`: Source-audited against OpenCLI 1.8.6 weibo/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
