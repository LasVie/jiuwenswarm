---
name: opencli-crates
description: Route reviewed Crates website operations through the OpenCLI Web structured execution boundary.
---

# Crates

Catalog site slug: `crates`.
 Known domains: `crates.io`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `crate` | `enabled` | `public_read` / `low` | `opencli_execute(site="crates", operation="public-data", command="crate", arguments={"name":"<name>"})`<br>Single crates.io crate metadata (latest version, downloads, license, repo) | `name` (str, required, positional) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="crates", operation="public-data", command="search", arguments={"query":"<query>"})`<br>Search the public crates.io registry by keyword | `query` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
