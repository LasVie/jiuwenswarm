# Chatgpt: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `status` | `private_account_read` / `medium` | `opencli chatgpt status -f json`<br>Check ChatGPT web page availability and login state | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli chatgpt whoami -f json`<br>Show the current logged-in chatgpt account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `status`: Source-audited against OpenCLI 1.8.6 chatgpt/status.js; reads current browser-session authentication state without changing it.; sensitive output: authentication state
- `whoami`: Source-audited against OpenCLI 1.8.6 chatgpt/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
