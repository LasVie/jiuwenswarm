# Linkedin Learning: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `trending` | `private_content_read` / `medium` | `opencli linkedin-learning trending [--limit <limit>] -f json`<br>Browse LinkedIn Learning recommended courses across personalized carousels | `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `trending`: Source-audited against OpenCLI 1.8.6 linkedin-learning/trending.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: personalized recommendations, account identifiers
