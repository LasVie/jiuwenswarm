---
name: opencli-1point3acres
description: Route reviewed 1Point3Acres website operations through the OpenCLI Web structured execution boundary.
---

# 1Point3Acres

Catalog site slug: `1point3acres`.
 Known domains: `1point3acres.com`, `www.1point3acres.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/1point3acres/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/1point3acres/operations/authentication.md` |
| `content` | Read site content and metadata. | `digest`, `forum`, `forums`, `hot`, `latest`, `thread`, `user` | `sites/1point3acres/operations/content.md` |
| `private-content` | Read content that depends on an authenticated account. | `notifications`, `search` | `sites/1point3acres/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
