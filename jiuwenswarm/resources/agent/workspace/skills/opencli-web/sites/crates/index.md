# Crates

- Site slug: `crates`
- Domains: `crates.io`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `crate`, `search` | `sites/crates/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `crate` | `public_read` / `low` | `opencli crates crate "<name>" -f json`<br>Single crates.io crate metadata (latest version, downloads, license, repo) | `name` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli crates search "<query>" [--limit <limit>] -f json`<br>Search the public crates.io registry by keyword | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
