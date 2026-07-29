---
name: opencli-facebook
description: Route reviewed Facebook website operations through the OpenCLI Web structured execution boundary.
---

# Facebook

Catalog site slug: `facebook`.
 Known domains: `facebook.com`, `www.facebook.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/facebook/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/facebook/operations/authentication.md` |
| `content` | Read site content and metadata. | `profile` | `sites/facebook/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `events`, `search` | `sites/facebook/operations/discovery.md` |
| `private-content` | Read content that depends on an authenticated account. | `feed`, `friends`, `groups`, `marketplace-inbox`, `marketplace-listings`, `memories`, `notifications` | `sites/facebook/operations/private-content.md` |
| `write-actions` | Change remote service state. | `add-friend`, `join-group` | `sites/facebook/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
