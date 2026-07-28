---
name: opencli-osv
description: Route reviewed Osv website operations through the OpenCLI Web structured execution boundary.
---

# Osv

Catalog site slug: `osv`.
 Known domains: `osv.dev`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `query` | `enabled` | `public_read` / `low` | `opencli_execute(site="osv", operation="public-data", command="query", arguments={"package":"<package>","ecosystem":"<ecosystem>"})`<br>OSV.dev vulnerabilities affecting a package (optionally pinned to a version) | `package` (string, required, positional); `ecosystem` (string, required); `version` (string, optional); `limit` (int, optional, default=30) |
| `vulnerability` | `enabled` | `public_read` / `low` | `opencli_execute(site="osv", operation="public-data", command="vulnerability", arguments={"id":"<id>"})`<br>Single OSV.dev vulnerability detail (severity, affected packages, CVE/GHSA aliases) | `id` (string, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
