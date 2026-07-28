---
name: opencli-guazi
description: Route reviewed Guazi website operations through the OpenCLI Web structured execution boundary.
---

# Guazi

Catalog site slug: `guazi`.
 Known domains: `m.guazi.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `browse` | `enabled` | `public_read` / `low` | `opencli_execute(site="guazi", operation="public-data", command="browse")`<br>瓜子二手车在售车源列表（按城市，含售价/首付/里程/年份） | `city` (str, optional, positional); `limit` (int, optional, default=20) |
| `car` | `enabled` | `public_read` / `low` | `opencli_execute(site="guazi", operation="public-data", command="car", arguments={"clue_id":"<clue_id>"})`<br>瓜子二手车车源详情（售价 / 上牌 / 里程 / 过户 / 配置 / 车况） | `clue_id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
