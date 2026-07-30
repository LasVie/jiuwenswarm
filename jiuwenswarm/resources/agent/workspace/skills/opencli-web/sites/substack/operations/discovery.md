# Substack: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `public_read` / `low` | `opencli substack feed [--category "<category>"] [--limit <limit>] -f json`<br>Substack 热门文章 Feed | `category` (str, optional, default='all'); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli substack search "<keyword>" [--type "<posts\|publications>"] [--limit <limit>] -f json`<br>搜索 Substack 文章和 Newsletter | `keyword` (str, required, positional); `type` (str, optional, default='posts', choices=posts,publications); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
