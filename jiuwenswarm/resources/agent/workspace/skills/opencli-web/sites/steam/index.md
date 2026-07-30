# Steam

- Site slug: `steam`
- Domains: `store.steampowered.com`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `app`, `search`, `top-sellers` | `sites/steam/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `app` | `public_read` / `low` | `opencli steam app "<id>" [--currency "<currency>"] -f json`<br>Steam storefront detail for a single app id | `id` (str, required, positional); `currency` (str, optional, default='us') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli steam search "<query>" [--limit <limit>] [--currency "<currency>"] -f json`<br>Search the Steam storefront by name keyword | `query` (str, required, positional); `limit` (int, optional, default=20); `currency` (str, optional, default='us') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top-sellers` | `public_read` / `low` | `opencli steam top-sellers [--limit <limit>] -f json`<br>Steam top selling games | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
