# Toutiao: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli toutiao hot [--limit <limit>] -f json`<br>今日头条首页热榜（公开 API，无需登录） | `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `recommend` | `public_read` / `low` | `opencli toutiao recommend [--category "<category>"] [--limit <limit>] -f json`<br>今日头条频道推荐流（公开 API，无需登录） | `category` (string, optional, default='__all__'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
