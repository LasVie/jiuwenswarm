# Manus: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `connectors` | `private_account_read` / `medium` | `opencli manus connectors [--limit <limit>] -f json`<br>List available Manus connectors (integrations). | `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `credits` | `private_account_read` / `medium` | `opencli manus credits -f json`<br>Show Manus credit balance and refresh details. | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `skills` | `private_account_read` / `medium` | `opencli manus skills -f json`<br>List Manus skills (user-added and system). | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `status` | `private_account_read` / `medium` | `opencli manus status -f json`<br>Show current Manus user profile and credit summary. | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli manus whoami -f json`<br>Show the current logged-in manus account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `connectors`: Source-audited against OpenCLI 1.8.6 manus/connectors.js; reads current browser-session or account-scoped metadata.; sensitive output: account configuration, account identifiers
- `credits`: Source-audited against OpenCLI 1.8.6 manus/credits.js; reads current browser-session or account-scoped metadata.; sensitive output: subscription and quota data, account identifiers
- `skills`: Source-audited against OpenCLI 1.8.6 manus/skills.js; reads current browser-session or account-scoped metadata.; sensitive output: account configuration, account identifiers
- `status`: Source-audited against OpenCLI 1.8.6 manus/status.js; reads current browser-session or account-scoped metadata.; sensitive output: authentication state, account identifiers
- `whoami`: Source-audited against OpenCLI 1.8.6 manus/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
