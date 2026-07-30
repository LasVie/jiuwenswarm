# Douban: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `book-hot` | `public_read` / `low` | `opencli douban book-hot [--limit <limit>] -f json`<br>豆瓣图书热门榜单 | `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `movie-hot` | `public_read` / `low` | `opencli douban movie-hot [--limit <limit>] -f json`<br>豆瓣电影热门榜单 | `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli douban search [--type "<movie\|book\|music>"] "<keyword>" [--limit <limit>] -f json`<br>搜索豆瓣电影、图书或音乐 | `type` (str, optional, default='movie', choices=movie,book,music); `keyword` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `top250` | `public_read` / `low` | `opencli douban top250 [--limit <limit>] -f json`<br>豆瓣电影 Top250 | `limit` (int, optional, default=250) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
