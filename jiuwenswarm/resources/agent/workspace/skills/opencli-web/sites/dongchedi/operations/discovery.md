# Dongchedi: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli dongchedi search "<keyword>" [--limit <limit>] -f json`<br>懂车帝车系搜索（按关键词，返回车系 + 指导价/经销商价） | `keyword` (str, required, positional); `limit` (int, optional, default=15) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
