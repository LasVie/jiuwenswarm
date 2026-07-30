# Tieba: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `read` | `public_read` / `low` | `opencli tieba read "<id>" [--page <page>] [--limit <limit>] -f json`<br>Read a tieba thread | `id` (string, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=30) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `read`: Source-audited against OpenCLI 1.8.6 tieba/read.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
