# 1Point3Acres: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `notifications` | `private_content_read` / `medium` | `opencli 1point3acres notifications [--kind "<kind>"] [--limit <limit>] -f json`<br>一亩三分地 站内通知（互动 / 点评 / @ 我；需要登录） | `kind` (string, optional, default='mypost'); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `notifications`: Source-audited against OpenCLI 1.8.6 1point3acres/notifications.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private notifications, account identifiers
