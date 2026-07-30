# Wikidata

- Site slug: `wikidata`
- Domains: `www.wikidata.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `entity`, `search` | `sites/wikidata/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `entity` | `public_read` / `low` | `opencli wikidata entity "<id>" [--language "<language>"] -f json`<br>Fetch a Wikidata entity by Q/P/L id (label, description, aliases, claim summary) | `id` (str, required, positional); `language` (str, optional, default='en') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli wikidata search "<query>" [--language "<language>"] [--limit <limit>] -f json`<br>Search Wikidata items by keyword (returns Q-IDs) | `query` (str, required, positional); `language` (str, optional, default='en'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
