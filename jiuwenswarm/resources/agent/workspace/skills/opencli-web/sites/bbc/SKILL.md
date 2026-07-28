---
name: opencli-bbc
description: Route reviewed Bbc website operations through the OpenCLI Web structured execution boundary.
---

# Bbc

Catalog site slug: `bbc`.
 Known domains: `www.bbc.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `news` | `enabled` | `public_read` / `low` | `opencli_execute(site="bbc", operation="public-data", command="news")`<br>BBC News headlines (RSS) | `limit` (int, optional, default=20) |
| `topic` | `enabled` | `public_read` / `low` | `opencli_execute(site="bbc", operation="public-data", command="topic", arguments={"topic":"<topic>"})`<br>BBC News headlines for a specific section (RSS feed) | `topic` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
