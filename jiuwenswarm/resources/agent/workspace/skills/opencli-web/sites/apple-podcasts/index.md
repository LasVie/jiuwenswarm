# Apple Podcasts

- Site slug: `apple-podcasts`
- Domains: `itunes.apple.com`, `rss.marketingtools.apple.com`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `episodes`, `search`, `top` | `sites/apple-podcasts/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `episodes` | `public_read` / `low` | `opencli apple-podcasts episodes "<id>" [--limit <limit>] -f json`<br>List recent episodes of an Apple Podcast (use ID from search) | `id` (str, required, positional); `limit` (int, optional, default=15) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli apple-podcasts search "<query>" [--limit <limit>] -f json`<br>Search Apple Podcasts | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top` | `public_read` / `low` | `opencli apple-podcasts top [--limit <limit>] [--country "<country>"] -f json`<br>Top podcasts chart on Apple Podcasts | `limit` (int, optional, default=20); `country` (str, optional, default='us') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
