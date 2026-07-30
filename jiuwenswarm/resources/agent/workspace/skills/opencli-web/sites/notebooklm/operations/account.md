# Notebooklm: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `status` | `private_account_read` / `medium` | `opencli notebooklm status -f json`<br>Check NotebookLM page availability and login state in the current Chrome session | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli notebooklm whoami -f json`<br>Show the current logged-in notebooklm account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `status`: Source-audited against OpenCLI 1.8.6 notebooklm/status.js; reads current browser-session authentication state without changing it.; sensitive output: account identifiers
- `whoami`: Source-audited against OpenCLI 1.8.6 notebooklm/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
