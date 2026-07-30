# Douban: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `photos` | `public_read` / `low` | `opencli douban photos "<id>" [--type "<type>"] [--limit <limit>] -f json`<br>获取电影海报/剧照图片列表 | `id` (str, required, positional); `type` (str, optional, default='Rb'); `limit` (int, optional, default=120) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `subject` | `public_read` / `low` | `opencli douban subject "<id>" [--type "<movie\|book>"] -f json`<br>获取豆瓣条目详情 | `id` (str, required, positional); `type` (str, optional, default='movie', choices=movie,book) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
