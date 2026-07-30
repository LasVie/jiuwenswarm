# Aibase: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `news` | `public_read` / `low` | `opencli aibase news [--limit <limit>] -f json`<br>AIbase 日报 - 每天三分钟关注AI行业趋势 | `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `news`: Source-audited against OpenCLI 1.8.6 aibase/news.js; reads public browser-rendered content without authenticated account state.
