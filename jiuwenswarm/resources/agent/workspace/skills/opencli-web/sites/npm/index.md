# Npm

- Site slug: `npm`
- Domains: `api.npmjs.org`, `registry.npmjs.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `downloads`, `package`, `search` | `sites/npm/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `downloads` | `public_read` / `low` | `opencli npm downloads "<name>" [--period "<period>"] -f json`<br>Daily download counts for an npm package over a window | `name` (str, required, positional); `period` (str, optional, default='last-week') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `package` | `public_read` / `low` | `opencli npm package "<name>" -f json`<br>Single npm package metadata (latest version, license, homepage, repository). Use `npm downloads` for stats. | `name` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli npm search "<query>" [--limit <limit>] -f json`<br>Search the public npm registry by keyword | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
