---
name: opencli-amazon
description: Route reviewed Amazon website operations through the OpenCLI Web structured execution boundary.
---

# Amazon

Catalog site slug: `amazon`.
 Known domains: `amazon.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/amazon/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/amazon/operations/authentication.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `new-releases` | `sites/amazon/operations/generation.md` |
| `private-content` | Read content that depends on an authenticated account. | `bestsellers`, `discussion`, `movers-shakers`, `offer`, `product`, `search` | `sites/amazon/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
