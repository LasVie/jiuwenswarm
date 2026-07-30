# V2Ex: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `notifications` | `private_content_read` / `medium` | `opencli v2ex notifications [--limit <limit>] -f json`<br>V2EX 获取提醒 (回复/由于) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `notifications`: Source-audited against OpenCLI 1.8.6 v2ex/notifications.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private notifications, account identifiers
