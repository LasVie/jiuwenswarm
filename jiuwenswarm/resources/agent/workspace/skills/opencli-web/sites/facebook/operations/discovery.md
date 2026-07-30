# Facebook: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `events` | `public_read` / `low` | `opencli facebook events [--limit <limit>] -f json`<br>Browse Facebook event categories | `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli facebook search "<query>" [--limit <limit>] -f json`<br>Search Facebook for people, pages, or posts | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
