# Duckduckgo: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli duckduckgo search "<keyword>" [--limit <limit>] [--offset <offset>] [--region "<region>"] [--time "<time>"] -f json`<br>Search DuckDuckGo | `keyword` (str, required, positional); `limit` (int, optional, default=10); `offset` (int, optional, default=0); `region` (str, optional); `time` (str, optional) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `suggest` | `public_read` / `low` | `opencli duckduckgo suggest "<keyword>" [--limit <limit>] -f json`<br>DuckDuckGo search suggestions | `keyword` (str, required, positional); `limit` (int, optional, default=8) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
