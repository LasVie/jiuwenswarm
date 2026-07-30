# Goproxy

- Site slug: `goproxy`
- Domains: `proxy.golang.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `module`, `versions` | `sites/goproxy/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `module` | `public_read` / `low` | `opencli goproxy module "<module>" -f json`<br>Latest version + VCS origin metadata for a Go module on proxy.golang.org | `module` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `versions` | `public_read` / `low` | `opencli goproxy versions "<module>" [--limit <limit>] [--with-time <true\|false>] -f json`<br>Published version tags for a Go module (newest first), optionally with publish times | `module` (string, required, positional); `limit` (int, optional, default=30); `with-time` (boolean, optional, default=False) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
