---
name: opencli-oeis
description: Route reviewed Oeis website operations through the OpenCLI Web structured execution boundary.
---

# Oeis

Catalog site slug: `oeis`.
 Known domains: `oeis.org`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="oeis", operation="public-data", command="search", arguments={"query":"<query>"})`<br>Search OEIS sequences by keyword or numeric pattern | `query` (str, required, positional); `limit` (int, optional, default=10) |
| `sequence` | `enabled` | `public_read` / `low` | `opencli_execute(site="oeis", operation="public-data", command="sequence", arguments={"id":"<id>"})`<br>Full OEIS sequence detail by A-number (terms, name, keywords, formula counts) | `id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
