# Xianyu: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli xianyu search "<query>" [--limit <limit>] [--min-price <min-price>] [--max-price <max-price>] [--province "<province>"] [--city "<city>"] -f json`<br>搜索闲鱼商品（支持服务端价格区间 / 地区筛选） | `query` (str, required, positional); `limit` (int, optional, default=20); `min-price` (float, optional); `max-price` (float, optional); `province` (string, optional); `city` (string, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
