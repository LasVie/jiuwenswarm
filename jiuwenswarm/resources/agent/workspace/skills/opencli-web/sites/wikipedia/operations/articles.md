# Wikipedia: articles

Read encyclopedia pages and summaries.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `page` | `public_read` / `low` | `opencli wikipedia page "<title>" [--lang "<lang>"] [--paragraphs <paragraphs>] -f json`<br>Full plain-text extract of a Wikipedia article (optional paragraph cap). | `title` (string, required, positional); `lang` (string, optional, default='en', pattern=^[a-z]{2,3}(?:-[a-z0-9]+)?$); `paragraphs` (int, optional, default=0, minimum=0) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `summary` | `public_read` / `low` | `opencli wikipedia summary "<title>" [--lang "<lang>"] -f json`<br>Get Wikipedia article summary | `title` (str, required, positional); `lang` (str, optional, default='en') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
