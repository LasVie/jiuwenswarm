# Oeis

- Site slug: `oeis`
- Domains: `oeis.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `search`, `sequence` | `sites/oeis/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli oeis search "<query>" [--limit <limit>] -f json`<br>Search OEIS sequences by keyword or numeric pattern | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `sequence` | `public_read` / `low` | `opencli oeis sequence "<id>" -f json`<br>Full OEIS sequence detail by A-number (terms, name, keywords, formula counts) | `id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
