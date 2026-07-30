# Rubygems

- Site slug: `rubygems`
- Domains: `rubygems.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `gem`, `search` | `sites/rubygems/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `gem` | `public_read` / `low` | `opencli rubygems gem "<name>" -f json`<br>Fetch a RubyGems.org gem's metadata (version, downloads, license, links) | `name` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli rubygems search "<query>" [--limit <limit>] -f json`<br>Search RubyGems.org gems by keyword | `query` (str, required, positional); `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
