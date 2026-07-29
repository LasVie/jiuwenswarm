---
name: opencli-mercury
description: Route reviewed Mercury website operations through the OpenCLI Web structured execution boundary.
---

# Mercury

Catalog site slug: `mercury`.
 Known domains: `app.mercury.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `check-login` | `sites/mercury/operations/account.md` |
| `financial-actions` | Financial or reimbursement state changes. | `reimbursement-draft` | `sites/mercury/operations/financial-actions.md` |
| `private-content` | Read content that depends on an authenticated account. | `reimbursement-plan` | `sites/mercury/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
