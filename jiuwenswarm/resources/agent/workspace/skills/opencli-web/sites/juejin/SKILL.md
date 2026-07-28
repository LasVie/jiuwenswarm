---
name: opencli-juejin
description: Route reviewed Juejin website operations through the OpenCLI Web structured execution boundary.
---

# Juejin

Catalog site slug: `juejin`.
 Known domains: `api.juejin.cn`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="juejin", operation="public-data", command="hot")`<br>Juejin (掘金) hot article ranking, optionally scoped to a category | `category` (string, optional); `limit` (int, optional, default=20) |
| `recommend` | `enabled` | `public_read` / `low` | `opencli_execute(site="juejin", operation="public-data", command="recommend")`<br>Juejin (掘金) homepage recommended article feed | `limit` (int, optional, default=20); `cursor` (string, optional, default='0') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
