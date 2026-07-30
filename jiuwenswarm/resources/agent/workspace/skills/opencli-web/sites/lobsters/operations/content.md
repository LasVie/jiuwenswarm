# Lobsters: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `active` | `public_read` / `low` | `opencli lobsters active [--limit <limit>] -f json`<br>Lobste.rs most active discussions | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `domain` | `public_read` / `low` | `opencli lobsters domain "<domain>" [--limit <limit>] -f json`<br>Lobste.rs stories submitted from a specific domain | `domain` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `hot` | `public_read` / `low` | `opencli lobsters hot [--limit <limit>] -f json`<br>Lobste.rs hottest stories | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `newest` | `public_read` / `low` | `opencli lobsters newest [--limit <limit>] -f json`<br>Lobste.rs newest stories | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `read` | `public_read` / `low` | `opencli lobsters read "<id>" [--limit <limit>] [--depth <depth>] [--replies <replies>] [--max-length <max-length>] -f json`<br>Read a Lobste.rs story and its comment tree | `id` (str, required, positional); `limit` (int, optional, default=25); `depth` (int, optional, default=2); `replies` (int, optional, default=5); `max-length` (int, optional, default=2000) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `tag` | `public_read` / `low` | `opencli lobsters tag "<tag>" [--limit <limit>] -f json`<br>Lobste.rs stories by tag | `tag` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
