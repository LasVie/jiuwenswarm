---
name: opencli-defillama
description: Route reviewed Defillama website operations through the OpenCLI Web structured execution boundary.
---

# Defillama

Catalog site slug: `defillama`.
 Known domains: `defillama.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `protocol` | `enabled` | `public_read` / `low` | `opencli_execute(site="defillama", operation="public-data", command="protocol", arguments={"slug":"<slug>"})`<br>Single DefiLlama protocol details (current TVL, mcap, chains, twitter, github, description) | `slug` (string, required, positional) |
| `protocols` | `enabled` | `public_read` / `low` | `opencli_execute(site="defillama", operation="public-data", command="protocols")`<br>Top DeFi protocols on DefiLlama by current TVL (slug, name, category, TVL, mcap, change_1d/7d, chains) | `limit` (int, optional, default=30) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
