---
name: opencli-weibo
description: Route reviewed Weibo website operations through the OpenCLI Web structured execution boundary.
---

# Weibo

Catalog site slug: `weibo`.
 Known domains: `weibo.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `me`, `whoami` | `sites/weibo/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/weibo/operations/authentication.md` |
| `content` | Read one public item, record, page, or resource. | `comments`, `post`, `user` | `sites/weibo/operations/content.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `delete` | `sites/weibo/operations/destructive-actions.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `hot`, `search`, `user-posts` | `sites/weibo/operations/discovery.md` |
| `private-content` | Read content that depends on an authenticated account. | `favorites`, `feed` | `sites/weibo/operations/private-content.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `publish` | `sites/weibo/operations/publishing.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
