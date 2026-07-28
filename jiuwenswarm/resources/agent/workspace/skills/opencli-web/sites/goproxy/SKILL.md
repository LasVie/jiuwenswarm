---
name: opencli-goproxy
description: Route reviewed Goproxy website operations through the OpenCLI Web structured execution boundary.
---

# Goproxy

Catalog site slug: `goproxy`.
 Known domains: `proxy.golang.org`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `module` | `enabled` | `public_read` / `low` | `opencli_execute(site="goproxy", operation="public-data", command="module", arguments={"module":"<module>"})`<br>Latest version + VCS origin metadata for a Go module on proxy.golang.org | `module` (string, required, positional) |
| `versions` | `enabled` | `public_read` / `low` | `opencli_execute(site="goproxy", operation="public-data", command="versions", arguments={"module":"<module>"})`<br>Published version tags for a Go module (newest first), optionally with publish times | `module` (string, required, positional); `limit` (int, optional, default=30); `with-time` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
