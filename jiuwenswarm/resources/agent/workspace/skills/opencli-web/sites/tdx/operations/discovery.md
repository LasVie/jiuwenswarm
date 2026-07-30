# Tdx: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot-rank` | `public_read` / `low` | `opencli tdx hot-rank [--limit <limit>] -f json`<br>通达信热搜榜 | `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `hot-rank`: Market-data read only; no trading authority and not investment advice.
