---
name: opencli-v2ex
description: Route reviewed V2Ex website operations through the OpenCLI Web structured execution boundary.
---

# V2Ex

Catalog site slug: `v2ex`.
 Known domains: `v2ex.com`, `www.v2ex.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `me`, `whoami` | `sites/v2ex/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `daily` | `sites/v2ex/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/v2ex/operations/authentication.md` |
| `content` | Read site content and metadata. | `hot`, `latest`, `member`, `node`, `nodes`, `replies`, `topic`, `user` | `sites/v2ex/operations/content.md` |
| `private-content` | Read content that depends on an authenticated account. | `notifications` | `sites/v2ex/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
