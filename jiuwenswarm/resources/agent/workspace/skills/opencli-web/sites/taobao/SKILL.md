---
name: opencli-taobao
description: Route reviewed Taobao website operations through the OpenCLI Web structured execution boundary.
---

# Taobao

Catalog site slug: `taobao`.
 Known domains: `cart.taobao.com`, `item.taobao.com`, `s.taobao.com`, `taobao.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/taobao/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `add-cart` | `sites/taobao/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/taobao/operations/authentication.md` |
| `private-content` | Read content that depends on an authenticated account. | `cart`, `detail`, `reviews`, `search` | `sites/taobao/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
