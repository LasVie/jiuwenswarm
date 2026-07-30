# Xiaohongshu: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli xiaohongshu ask "<query>" [--timeout <timeout>] [--source-limit <source-limit>] -f json`<br>Ask 小红书点点 and return the answer with citation sources. | `query` (str, required, positional); `timeout` (int, optional, default=90); `source-limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `feed` | `private_content_read` / `medium` | `opencli xiaohongshu feed [--limit <limit>] -f json`<br>小红书首页推荐 Feed (reads hydrated Pinia store) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `private_content_read` / `medium` | `opencli xiaohongshu search "<query>" [--limit <limit>] -f json`<br>搜索小红书笔记 | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `feed`: sensitive output: private content, account identifiers
- `search`: sensitive output: private content, account identifiers
