---
name: opencli-steam
description: Route reviewed Steam website operations through the OpenCLI Web structured execution boundary.
---

# Steam

Catalog site slug: `steam`.
 Known domains: `store.steampowered.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `app` | `enabled` | `public_read` / `low` | `opencli_execute(site="steam", operation="public-data", command="app", arguments={"id":"<id>"})`<br>Steam storefront detail for a single app id | `id` (str, required, positional); `currency` (str, optional, default='us') |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="steam", operation="public-data", command="search", arguments={"query":"<query>"})`<br>Search the Steam storefront by name keyword | `query` (str, required, positional); `limit` (int, optional, default=20); `currency` (str, optional, default='us') |
| `top-sellers` | `enabled` | `public_read` / `low` | `opencli_execute(site="steam", operation="public-data", command="top-sellers")`<br>Steam top selling games | `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
