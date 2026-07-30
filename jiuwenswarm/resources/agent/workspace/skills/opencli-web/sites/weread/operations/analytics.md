# Weread: analytics

Read aggregate metrics, trends, or rankings.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ranking` | `public_read` / `low` | `opencli weread ranking ["<category>"] [--limit <limit>] -f json`<br>WeRead book rankings by category | `category` (str, optional, positional, default='all'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
