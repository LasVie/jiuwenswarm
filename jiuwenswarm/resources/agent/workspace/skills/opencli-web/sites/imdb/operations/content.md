# Imdb: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `person` | `public_read` / `low` | `opencli imdb person "<id>" [--limit <limit>] -f json`<br>Get actor or director info | `id` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `reviews` | `public_read` / `low` | `opencli imdb reviews "<id>" [--limit <limit>] -f json`<br>Get user reviews for a movie or TV show | `id` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `title` | `public_read` / `low` | `opencli imdb title "<id>" -f json`<br>Get movie or TV show details | `id` (str, required, positional) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
