# Weixin: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli weixin search "<query>" [--page <page>] [--limit <limit>] -f json`<br>使用搜狗微信搜索公众号文章；如需导出正文 Markdown，请使用 weixin download 处理公众号文章链接 | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
