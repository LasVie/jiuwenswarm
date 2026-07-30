# Rest Countries

- Site slug: `rest-countries`
- Domains: `restcountries.com`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `country`, `region` | `sites/rest-countries/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `country` | `public_read` / `low` | `opencli rest-countries country "<name>" [--limit <limit>] -f json`<br>Look up countries by name (common / official, substring match) | `name` (str, required, positional); `limit` (int, optional, default=25) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `region` | `public_read` / `low` | `opencli rest-countries region "<region>" [--limit <limit>] -f json`<br>List countries in a region (africa / americas / asia / europe / oceania / antarctic) | `region` (str, required, positional); `limit` (int, optional, default=250) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
