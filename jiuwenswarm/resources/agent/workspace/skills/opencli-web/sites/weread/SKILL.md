---
name: opencli-weread
description: Route reviewed Weread website operations through the OpenCLI Web structured execution boundary.
---

# Weread

Catalog site slug: `weread`.
 Known domains: `weread.qq.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/weread/operations/account.md` |
| `analytics` | Read aggregate metrics, trends, or rankings. | `ranking` | `sites/weread/operations/analytics.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/weread/operations/authentication.md` |
| `content` | Read one public item, record, page, or resource. | `book` | `sites/weread/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `book-search`, `search` | `sites/weread/operations/discovery.md` |
| `private-content` | Read content that depends on an authenticated account. | `ai-outline`, `highlights`, `notebooks`, `notes`, `shelf` | `sites/weread/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
