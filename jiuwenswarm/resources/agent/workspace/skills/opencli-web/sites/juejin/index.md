# Juejin

- Site slug: `juejin`
- Domains: `api.juejin.cn`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `hot`, `recommend` | `sites/juejin/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli juejin hot [--category "<category>"] [--limit <limit>] -f json`<br>Juejin (掘金) hot article ranking, optionally scoped to a category | `category` (string, optional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `recommend` | `public_read` / `low` | `opencli juejin recommend [--limit <limit>] [--cursor "<cursor>"] -f json`<br>Juejin (掘金) homepage recommended article feed | `limit` (int, optional, default=20); `cursor` (string, optional, default='0') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
