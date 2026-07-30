# Archive: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli archive search "<query>" [--mediatype "<mediatype>"] [--sort "<sort>"] [--limit <limit>] -f json`<br>Search Internet Archive items across books, movies, audio, software, and web. | `query` (str, required, positional); `mediatype` (string, optional); `sort` (string, optional, default='downloads'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
