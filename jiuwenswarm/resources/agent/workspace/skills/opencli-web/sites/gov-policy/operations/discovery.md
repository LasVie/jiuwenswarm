# Gov Policy: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `recent` | `public_read` / `low` | `opencli gov-policy recent [--limit <limit>] -f json`<br>国务院最新政策文件 | `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli gov-policy search "<query>" [--limit <limit>] -f json`<br>中国政府网政策文件搜索 | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
