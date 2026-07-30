# Qwen: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `status` | `private_account_read` / `medium` | `opencli qwen status -f json`<br>Check Qianwen page availability, login state, current session and model | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli qwen whoami -f json`<br>Show the current logged-in qwen account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `status`: Source-audited against OpenCLI 1.8.6 qwen/status.js; reads current browser-session authentication state without changing it.; sensitive output: account identifiers
- `whoami`: Source-audited against OpenCLI 1.8.6 qwen/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
