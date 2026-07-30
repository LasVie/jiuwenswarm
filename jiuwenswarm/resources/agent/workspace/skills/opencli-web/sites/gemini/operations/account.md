# Gemini: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `models` | `private_account_read` / `medium` | `opencli gemini models -f json`<br>List available Gemini models from the web UI | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `status` | `private_account_read` / `medium` | `opencli gemini status -f json`<br>Check Gemini web page availability and login state | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli gemini whoami -f json`<br>Show the current logged-in gemini account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `models`: Source-audited against OpenCLI 1.8.6 gemini/models.js; reads browser-session model availability and account capabilities without changing the session.; sensitive output: account identifiers
- `status`: Source-audited against OpenCLI 1.8.6 gemini/status.js; reads current browser-session authentication state without changing it.; sensitive output: authentication state
- `whoami`: Source-audited against OpenCLI 1.8.6 gemini/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
