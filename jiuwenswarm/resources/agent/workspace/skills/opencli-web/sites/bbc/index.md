# Bbc

- Site slug: `bbc`
- Domains: `www.bbc.com`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `news`, `topic` | `sites/bbc/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `news` | `public_read` / `low` | `opencli bbc news [--limit <limit>] -f json`<br>BBC News headlines (RSS) | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `topic` | `public_read` / `low` | `opencli bbc topic "<topic>" [--limit <limit>] -f json`<br>BBC News headlines for a specific section (RSS feed) | `topic` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
