# Mercury: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `check-login` | `private_account_read` / `medium` | `opencli mercury check-login -f json`<br>Open Mercury reimbursements and report whether the active browser profile is logged in | none | auth=optional; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `check-login`: Source-audited against OpenCLI 1.8.6 mercury/check-login.js; reads current browser-session authentication state without changing it.; sensitive output: account identifiers
