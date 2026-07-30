# Weread: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `book-search` | `public_read` / `low` | `opencli weread book-search "<book>" "<query>" [--book-rank <book-rank>] [--limit <limit>] [--fragment-size <fragment-size>] [--raw <true\|false>] -f json`<br>Search within a WeRead book after resolving it by title | `book` (str, required, positional); `query` (str, required, positional); `book-rank` (int, optional, default=1); `limit` (int, optional, default=20); `fragment-size` (int, optional, default=150); `raw` (boolean, optional, default=False) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli weread search "<query>" [--limit <limit>] -f json`<br>Search books on WeRead | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
