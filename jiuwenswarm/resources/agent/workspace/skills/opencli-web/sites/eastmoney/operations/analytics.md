# Eastmoney: analytics

Read public rankings, market data, or analytical site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot-rank` | `public_read` / `low` | `opencli eastmoney hot-rank [--limit <limit>] -f json`<br>东方财富热股榜 | `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `hot-rank`: Source-audited against OpenCLI 1.8.6 eastmoney/hot-rank.js; reads public market-ranking data without placing orders; output is informational and not investment advice.
