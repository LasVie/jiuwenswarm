# Cnki: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli cnki search "<query>" [--limit <limit>] -f json`<br>中国知网论文搜索（海外版） | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
