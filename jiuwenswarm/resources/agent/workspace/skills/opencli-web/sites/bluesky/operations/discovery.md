# Bluesky: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli bluesky search "<query>" [--limit <limit>] -f json`<br>Search Bluesky users | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `trending` | `public_read` / `low` | `opencli bluesky trending [--limit <limit>] -f json`<br>Trending topics on Bluesky | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
