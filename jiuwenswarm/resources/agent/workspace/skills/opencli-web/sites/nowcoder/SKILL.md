---
name: opencli-nowcoder
description: Route reviewed Nowcoder website operations through the OpenCLI Web structured execution boundary.
---

# Nowcoder

Catalog site slug: `nowcoder`.
 Known domains: `nowcoder.com`, `www.nowcoder.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/nowcoder/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/nowcoder/operations/authentication.md` |
| `content` | Read site content and metadata. | `companies`, `creators`, `detail`, `experience`, `hot`, `jobs`, `papers`, `recommend`, `referral`, `salary`, `topics` | `sites/nowcoder/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search`, `suggest`, `trending` | `sites/nowcoder/operations/discovery.md` |
| `private-content` | Read content that depends on an authenticated account. | `notifications`, `practice` | `sites/nowcoder/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
