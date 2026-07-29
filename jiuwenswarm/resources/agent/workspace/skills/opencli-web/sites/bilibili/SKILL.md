---
name: opencli-bilibili
description: Route reviewed Bilibili website operations through the OpenCLI Web structured execution boundary.
---

# Bilibili

Catalog site slug: `bilibili`.
 Known domains: `www.bilibili.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `me`, `whoami` | `sites/bilibili/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `favorite`, `follow` | `sites/bilibili/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/bilibili/operations/authentication.md` |
| `content` | Read site content and metadata. | `comments`, `subtitle`, `summary`, `user-videos`, `video` | `sites/bilibili/operations/content.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `unfollow` | `sites/bilibili/operations/destructive-actions.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `hot`, `ranking`, `search` | `sites/bilibili/operations/discovery.md` |
| `file-operations` | Create or download workspace files. | `download` | `sites/bilibili/operations/file-operations.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `comment` | `sites/bilibili/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `dynamic`, `feed`, `feed-detail`, `following`, `history` | `sites/bilibili/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
