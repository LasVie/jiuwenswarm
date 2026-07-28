---
name: opencli-pypi
description: Route reviewed Pypi website operations through the OpenCLI Web structured execution boundary.
---

# Pypi

Catalog site slug: `pypi`.
 Known domains: `pypi.org`, `pypistats.org`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `downloads` | `enabled` | `public_read` / `low` | `opencli_execute(site="pypi", operation="public-data", command="downloads", arguments={"name":"<name>"})`<br>PyPI download stats for a package (recent totals or full daily history) | `name` (str, required, positional); `period` (str, optional, default='recent') |
| `package` | `enabled` | `public_read` / `low` | `opencli_execute(site="pypi", operation="public-data", command="package", arguments={"name":"<name>"})`<br>Single PyPI package metadata (latest version, license, homepage, classifiers) | `name` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
