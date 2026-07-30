# Packagist

- Site slug: `packagist`
- Domains: `packagist.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `package`, `search` | `sites/packagist/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `package` | `public_read` / `low` | `opencli packagist package "<name>" -f json`<br>Fetch a Packagist package's metadata (version, downloads, license, repo, GitHub stars) | `name` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli packagist search "<query>" [--limit <limit>] -f json`<br>Search Packagist (PHP / Composer) packages by keyword | `query` (str, required, positional); `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
