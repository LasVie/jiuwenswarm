---
name: opencli-wikidata
description: Route reviewed Wikidata website operations through the OpenCLI Web structured execution boundary.
---

# Wikidata

Catalog site slug: `wikidata`.
 Known domains: `www.wikidata.org`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `entity` | `enabled` | `public_read` / `low` | `opencli_execute(site="wikidata", operation="public-data", command="entity", arguments={"id":"<id>"})`<br>Fetch a Wikidata entity by Q/P/L id (label, description, aliases, claim summary) | `id` (str, required, positional); `language` (str, optional, default='en') |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="wikidata", operation="public-data", command="search", arguments={"query":"<query>"})`<br>Search Wikidata items by keyword (returns Q-IDs) | `query` (str, required, positional); `language` (str, optional, default='en'); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
