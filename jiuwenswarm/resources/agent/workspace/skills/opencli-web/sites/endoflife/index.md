# Endoflife

- Site slug: `endoflife`
- Domains: `endoflife.date`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `product` | `sites/endoflife/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `product` | `public_read` / `low` | `opencli endoflife product "<product>" -f json`<br>Release cycles + EOL / LTS / support dates for one product on endoflife.date | `product` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
