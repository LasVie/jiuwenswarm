# Ke: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `chengjiao` | `public_read` / `low` | `opencli ke chengjiao [--city "<city>"] [--district "<district>"] [--limit <limit>] -f json`<br>贝壳找房成交记录 | `city` (str, optional, default='bj'); `district` (str, optional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `ershoufang` | `public_read` / `low` | `opencli ke ershoufang [--city "<city>"] [--district "<district>"] [--min-price <min-price>] [--max-price <max-price>] [--rooms <rooms>] [--limit <limit>] -f json`<br>贝壳找房二手房列表 | `city` (str, optional, default='bj'); `district` (str, optional); `min-price` (int, optional); `max-price` (int, optional); `rooms` (int, optional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `xiaoqu` | `public_read` / `low` | `opencli ke xiaoqu [--city "<city>"] [--district "<district>"] [--limit <limit>] -f json`<br>贝壳找房小区列表 | `city` (str, optional, default='bj'); `district` (str, optional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `zufang` | `public_read` / `low` | `opencli ke zufang [--city "<city>"] [--district "<district>"] [--min-price <min-price>] [--max-price <max-price>] [--limit <limit>] -f json`<br>贝壳找房租房列表 | `city` (str, optional, default='bj'); `district` (str, optional); `min-price` (int, optional); `max-price` (int, optional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
