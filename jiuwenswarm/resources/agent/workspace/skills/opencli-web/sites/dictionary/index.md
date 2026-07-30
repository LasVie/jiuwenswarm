# Dictionary

- Site slug: `dictionary`
- Domains: `api.dictionaryapi.dev`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `examples`, `search`, `synonyms` | `sites/dictionary/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `examples` | `public_read` / `low` | `opencli dictionary examples "<word>" -f json`<br>Read real-world example sentences utilizing the word | `word` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli dictionary search "<word>" -f json`<br>Search the Free Dictionary API for definitions, parts of speech, and pronunciations. | `word` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `synonyms` | `public_read` / `low` | `opencli dictionary synonyms "<word>" -f json`<br>Find synonyms for a specific word | `word` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
