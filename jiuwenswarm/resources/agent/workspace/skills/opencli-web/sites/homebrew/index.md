# Homebrew

- Site slug: `homebrew`
- Domains: `formulae.brew.sh`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `cask`, `formula`, `popular` | `sites/homebrew/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `cask` | `public_read` / `low` | `opencli homebrew cask "<token>" -f json`<br>Fetch a Homebrew cask's metadata (version, homepage, deprecation, download URL) | `token` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `formula` | `public_read` / `low` | `opencli homebrew formula "<name>" -f json`<br>Fetch a Homebrew formula's metadata (version, license, deps, deprecation, source) | `name` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `popular` | `public_read` / `low` | `opencli homebrew popular [--type "<type>"] [--window "<window>"] [--limit <limit>] -f json`<br>List most-installed Homebrew formulae or casks (Homebrew's analytics ranking) | `type` (str, optional, default='formula'); `window` (str, optional, default='30d'); `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
