---
name: opencli-ctrip
description: Route reviewed Ctrip website operations through the OpenCLI Web structured execution boundary.
---

# Ctrip

Catalog site slug: `ctrip`.
 Known domains: `ctrip.com`, `flights.ctrip.com`, `hotels.ctrip.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/ctrip/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/ctrip/operations/authentication.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `hotel-suggest`, `search` | `sites/ctrip/operations/discovery.md` |
| `private-content` | Read content that depends on an authenticated account. | `flight`, `hotel-search` | `sites/ctrip/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
