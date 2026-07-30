# Tvmaze

- Site slug: `tvmaze`
- Domains: `tvmaze.com`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `search`, `show` | `sites/tvmaze/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli tvmaze search "<query>" [--limit <limit>] -f json`<br>TVmaze TV show search by title (returns id, name, network, premiered/ended, rating) | `query` (string, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `show` | `public_read` / `low` | `opencli tvmaze show <id> -f json`<br>Single TVmaze TV show detail by id (network, schedule, rating, IMDB/TheTVDB cross-refs) | `id` (int, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
