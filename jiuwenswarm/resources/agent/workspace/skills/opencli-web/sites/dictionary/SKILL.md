---
name: opencli-dictionary
description: Route reviewed Dictionary website operations through the OpenCLI Web structured execution boundary.
---

# Dictionary

Catalog site slug: `dictionary`.
 Known domains: `api.dictionaryapi.dev`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `examples` | `enabled` | `public_read` / `low` | `opencli_execute(site="dictionary", operation="public-data", command="examples", arguments={"word":"<word>"})`<br>Read real-world example sentences utilizing the word | `word` (string, required, positional) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="dictionary", operation="public-data", command="search", arguments={"word":"<word>"})`<br>Search the Free Dictionary API for definitions, parts of speech, and pronunciations. | `word` (string, required, positional) |
| `synonyms` | `enabled` | `public_read` / `low` | `opencli_execute(site="dictionary", operation="public-data", command="synonyms", arguments={"word":"<word>"})`<br>Find synonyms for a specific word | `word` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
