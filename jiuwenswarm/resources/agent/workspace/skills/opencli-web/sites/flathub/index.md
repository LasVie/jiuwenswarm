# Flathub

- Site slug: `flathub`
- Domains: `flathub.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `app`, `search` | `sites/flathub/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `app` | `public_read` / `low` | `opencli flathub app "<appId>" -f json`<br>Full Flathub appstream metadata for an app id (license, categories, latest release) | `appId` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli flathub search "<query>" [--limit <limit>] -f json`<br>Search Flathub apps by keyword | `query` (str, required, positional); `limit` (int, optional, default=25) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
