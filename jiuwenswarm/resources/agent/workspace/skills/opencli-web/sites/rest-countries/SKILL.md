---
name: opencli-rest-countries
description: Route reviewed Rest Countries website operations through the OpenCLI Web structured execution boundary.
---

# Rest Countries

Catalog site slug: `rest-countries`.
 Known domains: `restcountries.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `country` | `enabled` | `public_read` / `low` | `opencli_execute(site="rest-countries", operation="public-data", command="country", arguments={"name":"<name>"})`<br>Look up countries by name (common / official, substring match) | `name` (str, required, positional); `limit` (int, optional, default=25) |
| `region` | `enabled` | `public_read` / `low` | `opencli_execute(site="rest-countries", operation="public-data", command="region", arguments={"region":"<region>"})`<br>List countries in a region (africa / americas / asia / europe / oceania / antarctic) | `region` (str, required, positional); `limit` (int, optional, default=250) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
