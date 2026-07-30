# Weibo: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `favorites` | `private_content_read` / `medium` | `opencli weibo favorites [--limit <limit>] -f json`<br>我的微博收藏列表 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `feed` | `private_content_read` / `medium` | `opencli weibo feed [--type "<for-you\|following>"] [--limit <limit>] -f json`<br>Fetch Weibo timeline (for-you or following) | `type` (str, optional, default='for-you', choices=for-you,following); `limit` (int, optional, default=15) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `favorites`: Source-audited against OpenCLI 1.8.6 weibo/favorites.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private social content, account identifiers
- `feed`: Source-audited against OpenCLI 1.8.6 weibo/feed.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private social content, account identifiers
