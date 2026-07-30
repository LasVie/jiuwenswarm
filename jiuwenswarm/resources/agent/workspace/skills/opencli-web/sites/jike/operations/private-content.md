# Jike: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `private_content_read` / `medium` | `opencli jike feed [--limit <limit>] -f json`<br>即刻首页动态流 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notifications` | `private_content_read` / `medium` | `opencli jike notifications [--limit <limit>] -f json`<br>即刻通知 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `feed`: Source-audited against OpenCLI 1.8.6 jike/feed.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private social content, account identifiers
- `notifications`: Source-audited against OpenCLI 1.8.6 jike/notifications.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private social content, account identifiers
