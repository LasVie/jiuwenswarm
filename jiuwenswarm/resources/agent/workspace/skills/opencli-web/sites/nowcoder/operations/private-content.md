# Nowcoder: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `notifications` | `private_content_read` / `medium` | `opencli nowcoder notifications -f json`<br>Unread message summary | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `practice` | `private_content_read` / `medium` | `opencli nowcoder practice [--job "<job>"] [--limit <limit>] -f json`<br>Categorized practice questions with progress | `job` (str, optional, default='11226'); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `notifications`: Source-audited against OpenCLI 1.8.6 nowcoder/notifications.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private notifications, account identifiers
- `practice`: Source-audited against OpenCLI 1.8.6 nowcoder/practice.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: learning progress, account identifiers
