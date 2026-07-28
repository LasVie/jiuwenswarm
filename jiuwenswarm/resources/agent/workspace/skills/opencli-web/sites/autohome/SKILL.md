---
name: opencli-autohome
description: Route reviewed Autohome website operations through the OpenCLI Web structured execution boundary.
---

# Autohome

Catalog site slug: `autohome`.
 Known domains: catalog did not declare one.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `brand` | `enabled` | `public_read` / `low` | `opencli_execute(site="autohome", operation="public-data", command="brand", arguments={"brand":"<brand>"})`<br>汽车之家按品牌列出全部车系 + 厂商指导价（免登录） | `brand` (str, required, positional); `limit` (int, optional, default=60) |
| `score` | `enabled` | `public_read` / `low` | `opencli_execute(site="autohome", operation="public-data", command="score", arguments={"series_id":"<series_id>"})`<br>汽车之家车系口碑评分（总分 + 各维度 + 故障率PPH + 竞品对比，免登录） | `series_id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
