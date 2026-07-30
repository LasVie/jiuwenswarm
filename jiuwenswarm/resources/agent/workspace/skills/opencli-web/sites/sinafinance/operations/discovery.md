# Sinafinance: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `news` | `public_read` / `low` | `opencli sinafinance news [--limit <limit>] [--type <type>] -f json`<br>新浪财经 7x24 小时实时快讯 | `limit` (int, optional, default=20); `type` (int, optional, default=0) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `rolling-news` | `public_read` / `low` | `opencli sinafinance rolling-news -f json`<br>新浪财经滚动新闻 | none | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `stock-rank` | `public_read` / `low` | `opencli sinafinance stock-rank [--market "<cn\|hk\|us\|wh\|ft>"] -f json`<br>新浪财经热搜榜 | `market` (string, optional, default='cn', choices=cn,hk,us,wh,ft) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `news`: Market-data read only; no trading authority and not investment advice.
- `rolling-news`: Market-data read only; no trading authority and not investment advice.
- `stock-rank`: Market-data read only; no trading authority and not investment advice.
