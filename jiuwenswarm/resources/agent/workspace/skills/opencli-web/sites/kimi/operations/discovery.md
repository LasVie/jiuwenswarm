# Kimi: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `templates` | `public_read` / `low` | `opencli kimi templates [--mode "<mode>"] [--limit <limit>] -f json`<br>List template cards visible on a Kimi mode page (PPT/docs/deep-research/agent). Each mode shows curated example projects organized by category. Pass --mode to navigate first. | `mode` (str, optional); `limit` (int, optional, default=30) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `templates`: Source-audited against OpenCLI 1.8.6 kimi/audit-extras.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
