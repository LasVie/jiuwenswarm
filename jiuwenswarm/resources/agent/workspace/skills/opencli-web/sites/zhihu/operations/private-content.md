# Zhihu: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `collection` | `private_content_read` / `medium` | `opencli zhihu collection "<id>" [--offset <offset>] [--limit <limit>] -f json`<br>知乎收藏夹内容列表（需要登录） | `id` (str, required, positional); `offset` (int, optional, default=0); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `collections` | `private_content_read` / `medium` | `opencli zhihu collections [--limit <limit>] -f json`<br>知乎收藏夹列表（需要登录） | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `recommend` | `private_content_read` / `medium` | `opencli zhihu recommend [--limit <limit>] -f json`<br>知乎首页推荐 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `collection`: Source-audited against OpenCLI 1.8.6 zhihu/collection.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private social content, account identifiers
- `collections`: Source-audited against OpenCLI 1.8.6 zhihu/collections.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private social content, account identifiers
- `recommend`: Source-audited against OpenCLI 1.8.6 zhihu/recommend.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private social content, account identifiers
