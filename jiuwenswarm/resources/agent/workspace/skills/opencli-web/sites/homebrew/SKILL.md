---
name: opencli-homebrew
description: Route reviewed Homebrew website operations through the OpenCLI Web structured execution boundary.
---

# Homebrew

Catalog site slug: `homebrew`.
 Known domains: `formulae.brew.sh`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Terminal site contract

This compact site router is also the terminal execution contract. Its single operation has one low-risk public-read boundary. A successful exact SkillTool read of this path is required before `opencli_execute`.

Logical operation: `public-data` — Read low-risk public data without browser state.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `cask` | `enabled` | `public_read` / `low` | `opencli_execute(site="homebrew", operation="public-data", command="cask", arguments={"token":"<token>"})`<br>Fetch a Homebrew cask's metadata (version, homepage, deprecation, download URL) | `token` (str, required, positional) |
| `formula` | `enabled` | `public_read` / `low` | `opencli_execute(site="homebrew", operation="public-data", command="formula", arguments={"name":"<name>"})`<br>Fetch a Homebrew formula's metadata (version, license, deps, deprecation, source) | `name` (str, required, positional) |
| `popular` | `enabled` | `public_read` / `low` | `opencli_execute(site="homebrew", operation="public-data", command="popular")`<br>List most-installed Homebrew formulae or casks (Homebrew's analytics ranking) | `type` (str, optional, default='formula'); `window` (str, optional, default='30d'); `limit` (int, optional, default=30) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
