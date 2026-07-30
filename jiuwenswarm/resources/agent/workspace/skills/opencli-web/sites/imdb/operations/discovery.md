# Imdb: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli imdb search "<query>" [--limit <limit>] -f json`<br>Search IMDb for movies, TV shows, and people | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `top` | `public_read` / `low` | `opencli imdb top [--limit <limit>] -f json`<br>IMDb Top 250 Movies | `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `trending` | `public_read` / `low` | `opencli imdb trending [--limit <limit>] -f json`<br>IMDb Most Popular Movies | `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
