---
name: opencli-apple-podcasts
description: Route reviewed Apple Podcasts website operations through the OpenCLI Web structured execution boundary.
---

# Apple Podcasts

Catalog site slug: `apple-podcasts`.
 Known domains: catalog did not declare one.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `episodes` | `enabled` | `public_read` / `low` | `opencli_execute(site="apple-podcasts", operation="public-data", command="episodes", arguments={"id":"<id>"})`<br>List recent episodes of an Apple Podcast (use ID from search) | `id` (str, required, positional); `limit` (int, optional, default=15) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="apple-podcasts", operation="public-data", command="search", arguments={"query":"<query>"})`<br>Search Apple Podcasts | `query` (str, required, positional); `limit` (int, optional, default=10) |
| `top` | `enabled` | `public_read` / `low` | `opencli_execute(site="apple-podcasts", operation="public-data", command="top")`<br>Top podcasts chart on Apple Podcasts | `limit` (int, optional, default=20); `country` (str, optional, default='us') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
