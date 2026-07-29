---
name: opencli-ones
description: Route reviewed Ones website operations through the OpenCLI Web structured execution boundary.
---

# Ones

Catalog site slug: `ones`.
 Known domains: `ones.cn`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `me`, `token-info` | `sites/ones/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login`, `logout` | `sites/ones/operations/authentication.md` |
| `private-content` | Read content that depends on an authenticated account. | `my-tasks`, `task`, `tasks` | `sites/ones/operations/private-content.md` |
| `write-actions` | Change remote service state. | `worklog` | `sites/ones/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
