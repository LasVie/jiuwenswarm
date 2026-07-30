# Hupu: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `mentions` | `private_content_read` / `medium` | `opencli hupu mentions [--limit <limit>] [--max_pages <max_pages>] [--page_str "<page_str>"] -f json`<br>查看虎扑提到我的回复 (需要登录) | `limit` (int, optional, default=20); `max_pages` (int, optional, default=3); `page_str` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `mentions`: Source-audited against OpenCLI 1.8.6 hupu/mentions.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private notifications, account identifiers
