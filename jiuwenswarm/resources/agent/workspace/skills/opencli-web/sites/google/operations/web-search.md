# Google: web-search

Read browser-rendered web search results.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli google search "<keyword>" [--limit <limit>] [--lang "<lang>"] -f json`<br>Search Google | `keyword` (str, required, positional); `limit` (int, optional, default=10, minimum=1,maximum=100); `lang` (str, optional, default='en') | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
