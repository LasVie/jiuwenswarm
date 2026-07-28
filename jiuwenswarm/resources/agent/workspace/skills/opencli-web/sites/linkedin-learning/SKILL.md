---
name: opencli-linkedin-learning
description: Route reviewed Linkedin Learning website operations through the OpenCLI Web structured execution boundary.
---

# Linkedin Learning

Catalog site slug: `linkedin-learning`.
 Known domains: `linkedin.com`, `www.linkedin.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/linkedin-learning/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/linkedin-learning/operations/authentication.md` |
| `private-content` | Read content that depends on an authenticated account. | `course`, `search`, `trending` | `sites/linkedin-learning/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
