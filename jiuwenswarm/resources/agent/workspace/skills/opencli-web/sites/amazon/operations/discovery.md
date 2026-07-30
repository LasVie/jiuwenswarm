# Amazon: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `bestsellers` | `public_read` / `low` | `opencli amazon bestsellers ["<input>"] [--limit <limit>] -f json`<br>Amazon Best Sellers pages for category candidate discovery | `input` (str, optional, positional); `limit` (int, optional, default=100) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `movers-shakers` | `public_read` / `low` | `opencli amazon movers-shakers ["<input>"] [--limit <limit>] -f json`<br>Amazon Movers & Shakers pages for short-term growth signals | `input` (str, optional, positional); `limit` (int, optional, default=100) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new-releases` | `public_read` / `low` | `opencli amazon new-releases ["<input>"] [--limit <limit>] -f json`<br>Amazon New Releases pages for early momentum discovery | `input` (str, optional, positional); `limit` (int, optional, default=100) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli amazon search "<query>" [--limit <limit>] -f json`<br>Amazon search results for product discovery and coarse filtering | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
