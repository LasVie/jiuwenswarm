---
name: opencli-tiktok
description: Route reviewed Tiktok website operations through the OpenCLI Web structured execution boundary.
---

# Tiktok

Catalog site slug: `tiktok`.
 Known domains: `tiktok.com`, `www.tiktok.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/tiktok/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `follow`, `like`, `save` | `sites/tiktok/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/tiktok/operations/authentication.md` |
| `content` | Read site content and metadata. | `profile`, `user` | `sites/tiktok/operations/content.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `unfollow` | `sites/tiktok/operations/destructive-actions.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `explore`, `live`, `search` | `sites/tiktok/operations/discovery.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `comment` | `sites/tiktok/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `creator-videos`, `following`, `friends`, `notifications` | `sites/tiktok/operations/private-content.md` |
| `write-actions` | Change remote service state. | `unlike`, `unsave` | `sites/tiktok/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
