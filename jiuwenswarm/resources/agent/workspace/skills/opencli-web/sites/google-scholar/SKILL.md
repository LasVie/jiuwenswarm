---
name: opencli-google-scholar
description: Route reviewed Google Scholar website operations through the OpenCLI Web structured execution boundary.
---

# Google Scholar

Catalog site slug: `google-scholar`.
 Known domains: `scholar.google.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `profile` | `sites/google-scholar/operations/account.md` |
| `private-content` | Read content that depends on an authenticated account. | `cite`, `search` | `sites/google-scholar/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
