# Hackernews: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli hackernews search "<query>" [--limit <limit>] [--sort "<relevance\|date>"] -f json`<br>Search Hacker News stories | `query` (str, required, positional); `limit` (int, optional, default=20); `sort` (str, optional, default='relevance', choices=relevance,date) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
