# Xianyu: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `item` | `public_read` / `low` | `opencli xianyu item "<item_id>" -f json`<br>查看闲鱼商品详情 | `item_id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
