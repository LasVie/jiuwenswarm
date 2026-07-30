# Bilibili: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli bilibili hot [--limit <limit>] -f json`<br>B站热门视频 | `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `ranking` | `public_read` / `low` | `opencli bilibili ranking [--limit <limit>] -f json`<br>Get Bilibili video ranking board | `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli bilibili search "<query>" [--type "<type>"] [--page <page>] [--limit <limit>] -f json`<br>Search Bilibili videos or users | `query` (str, required, positional); `type` (str, optional, default='video'); `page` (int, optional, default=1); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
