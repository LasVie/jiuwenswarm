# Trip: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli trip search "<query>" [--limit <limit>] -f json`<br>Suggest Trip.com destinations (cities, airports) for a keyword; resolves the ids the other commands take | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
