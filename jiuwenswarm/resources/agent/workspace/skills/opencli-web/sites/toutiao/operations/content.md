# Toutiao: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli toutiao hot [--limit <limit>] -f json`<br>今日头条首页热榜（公开 API，无需登录） | `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
