---
name: opencli-nvd
description: Route reviewed Nvd website operations through the OpenCLI Web structured execution boundary.
---

# Nvd

Catalog site slug: `nvd`.
 Known domains: `services.nvd.nist.gov`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `cve` | `enabled` | `public_read` / `low` | `opencli_execute(site="nvd", operation="public-data", command="cve", arguments={"id":"<id>"})`<br>NIST NVD CVE detail (description, CVSS, CWE, KEV flag) | `id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
