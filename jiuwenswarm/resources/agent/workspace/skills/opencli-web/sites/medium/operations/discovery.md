# Medium: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `public_read` / `low` | `opencli medium feed [--topic "<topic>"] [--limit <limit>] -f json`<br>Medium 热门文章 Feed | `topic` (str, optional, default=''); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli medium search "<keyword>" [--limit <limit>] -f json`<br>搜索 Medium 文章 | `keyword` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
