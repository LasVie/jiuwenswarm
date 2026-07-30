# Wttr

- Site slug: `wttr`
- Domains: `wttr.in`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `current`, `forecast` | `sites/wttr/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `current` | `public_read` / `low` | `opencli wttr current "<location>" -f json`<br>Current weather conditions for a location (city, lat,lon, or airport code) | `location` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `forecast` | `public_read` / `low` | `opencli wttr forecast "<location>" [--days <days>] -f json`<br>Multi-day weather forecast (up to 3 days, wttr.in free tier max) | `location` (str, required, positional); `days` (int, optional, default=3) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
