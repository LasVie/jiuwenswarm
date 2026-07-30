# Doubao: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `status` | `private_account_read` / `medium` | `opencli doubao status -f json`<br>Check Doubao chat page availability and login state | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli doubao whoami -f json`<br>Show the current logged-in doubao account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `status`: Source-audited against OpenCLI 1.8.6 doubao/status.js; reads current browser-session authentication state without changing it.; sensitive output: account identifiers
- `whoami`: Source-audited against OpenCLI 1.8.6 doubao/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
