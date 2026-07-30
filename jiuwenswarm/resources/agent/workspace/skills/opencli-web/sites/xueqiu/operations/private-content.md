# Xueqiu: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `private_content_read` / `medium` | `opencli xueqiu feed [--page <page>] [--limit <limit>] -f json`<br>获取雪球首页时间线（关注用户的动态） | `page` (int, optional, default=1); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `feed`: Source-audited against OpenCLI 1.8.6 xueqiu/feed.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: personalized financial feed, account identifiers
