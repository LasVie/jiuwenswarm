# Openreview: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli openreview search "<query>" [--limit <limit>] -f json`<br>Search OpenReview papers by free-text query | `query` (str, required, positional); `limit` (int, optional, default=25) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
