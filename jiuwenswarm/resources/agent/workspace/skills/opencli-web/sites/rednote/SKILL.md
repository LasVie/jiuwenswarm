---
name: opencli-rednote
description: Route reviewed Rednote website operations through the OpenCLI Web structured execution boundary.
---

# Rednote

Catalog site slug: `rednote`.
 Known domains: `rednote.com`, `www.rednote.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/rednote/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/rednote/operations/authentication.md` |
| `content` | Read site content and metadata. | `comments`, `note`, `user` | `sites/rednote/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search` | `sites/rednote/operations/discovery.md` |
| `file-operations` | Create or download workspace files. | `download` | `sites/rednote/operations/file-operations.md` |
| `private-content` | Read content that depends on an authenticated account. | `feed`, `notifications` | `sites/rednote/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
