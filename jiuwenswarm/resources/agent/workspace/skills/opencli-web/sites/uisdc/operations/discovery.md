# Uisdc: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `news` | `public_read` / `low` | `opencli uisdc news [--limit <limit>] -f json`<br>优设读报 - 最新 AI/设计行业新闻 | `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
