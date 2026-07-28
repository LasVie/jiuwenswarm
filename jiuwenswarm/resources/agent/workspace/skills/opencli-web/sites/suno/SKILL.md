---
name: opencli-suno
description: Route reviewed Suno website operations through the OpenCLI Web structured execution boundary.
---

# Suno

Catalog site slug: `suno`.
 Known domains: `suno.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/suno/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/suno/operations/authentication.md` |
| `file-operations` | Create or download workspace files. | `download` | `sites/suno/operations/file-operations.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `generate` | `sites/suno/operations/generation.md` |
| `private-content` | Read content that depends on an authenticated account. | `list`, `status` | `sites/suno/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
