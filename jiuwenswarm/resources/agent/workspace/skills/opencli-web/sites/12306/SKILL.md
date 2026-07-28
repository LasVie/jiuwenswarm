---
name: opencli-12306
description: Route reviewed 12306 website operations through the OpenCLI Web structured execution boundary.
---

# 12306

Catalog site slug: `12306`.
 Known domains: `12306.cn`, `kyfw.12306.cn`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `me`, `whoami` | `sites/12306/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/12306/operations/authentication.md` |
| `content` | Read site content and metadata. | `price`, `stations`, `train`, `trains` | `sites/12306/operations/content.md` |
| `private-content` | Read content that depends on an authenticated account. | `orders`, `passengers` | `sites/12306/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
