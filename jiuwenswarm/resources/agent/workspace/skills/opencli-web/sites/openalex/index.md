# Openalex

- Site slug: `openalex`
- Domains: `api.openalex.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `search`, `work` | `sites/openalex/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli openalex search "<query>" [--limit <limit>] -f json`<br>Search OpenAlex Works (papers, books, preprints) by keyword | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `work` | `public_read` / `low` | `opencli openalex work "<id>" -f json`<br>Fetch a single OpenAlex Work (paper / preprint / book) — metadata + abstract | `id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
