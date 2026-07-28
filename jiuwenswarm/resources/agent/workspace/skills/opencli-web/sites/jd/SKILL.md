---
name: opencli-jd
description: Route reviewed Jd website operations through the OpenCLI Web structured execution boundary.
---

# Jd

Catalog site slug: `jd`.
 Known domains: `cart.jd.com`, `item.jd.com`, `jd.com`, `search.jd.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/jd/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `add-cart` | `sites/jd/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/jd/operations/authentication.md` |
| `private-content` | Read content that depends on an authenticated account. | `cart`, `detail`, `item`, `reviews`, `search` | `sites/jd/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
