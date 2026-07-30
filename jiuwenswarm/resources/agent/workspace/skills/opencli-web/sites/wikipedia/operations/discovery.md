# Wikipedia: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `random` | `public_read` / `low` | `opencli wikipedia random [--lang "<lang>"] -f json`<br>Get a random Wikipedia article | `lang` (str, optional, default='en') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli wikipedia search "<query>" [--limit <limit>] [--lang "<lang>"] -f json`<br>Search Wikipedia articles | `query` (str, required, positional); `limit` (int, optional, default=10, minimum=1,maximum=50); `lang` (str, optional, default='en', pattern=^[a-z]{2,3}(?:-[a-z0-9]+)?$) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `trending` | `public_read` / `low` | `opencli wikipedia trending [--limit <limit>] [--lang "<lang>"] -f json`<br>Most-read Wikipedia articles (yesterday) | `limit` (int, optional, default=10, minimum=1,maximum=50); `lang` (str, optional, default='en', pattern=^[a-z]{2,3}(?:-[a-z0-9]+)?$) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
