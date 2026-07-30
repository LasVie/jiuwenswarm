# Sinablog: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli sinablog hot [--limit <limit>] -f json`<br>获取新浪博客热门文章/推荐 | `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli sinablog search "<keyword>" [--limit <limit>] -f json`<br>搜索新浪博客文章（通过新浪搜索） | `keyword` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
