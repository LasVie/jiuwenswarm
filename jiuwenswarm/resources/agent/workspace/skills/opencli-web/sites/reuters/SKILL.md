---
name: opencli-reuters
description: Route reviewed Reuters website operations through the OpenCLI Web structured execution boundary.
---

# Reuters

Catalog site slug: `reuters`.
 Known domains: `reuters.com`, `www.reuters.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/reuters/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/reuters/operations/authentication.md` |
| `content` | Read one public item, record, page, or resource. | `article-detail` | `sites/reuters/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search` | `sites/reuters/operations/discovery.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
