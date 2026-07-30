# Mdn

- Site slug: `mdn`
- Domains: `developer.mozilla.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `search` | `sites/mdn/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli mdn search "<query>" [--limit <limit>] [--locale "<locale>"] -f json`<br>Search MDN Web Docs by keyword | `query` (str, required, positional); `limit` (int, optional, default=10); `locale` (str, optional, default='en-US') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
