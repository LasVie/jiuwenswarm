# Rfc

- Site slug: `rfc`
- Domains: `datatracker.ietf.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `rfc` | `sites/rfc/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `rfc` | `public_read` / `low` | `opencli rfc rfc <number> -f json`<br>Single IETF RFC metadata (title, abstract, working group, authors, std level) | `number` (int, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
