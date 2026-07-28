---
name: opencli-quark
description: Route reviewed Quark website operations through the OpenCLI Web structured execution boundary.
---

# Quark

Catalog site slug: `quark`.
 Known domains: `pan.quark.cn`, `quark.cn`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/quark/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `save` | `sites/quark/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/quark/operations/authentication.md` |
| `private-content` | Read content that depends on an authenticated account. | `ls`, `share-tree` | `sites/quark/operations/private-content.md` |
| `write-actions` | Change remote service state. | `mkdir`, `mv`, `rename`, `rm` | `sites/quark/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
