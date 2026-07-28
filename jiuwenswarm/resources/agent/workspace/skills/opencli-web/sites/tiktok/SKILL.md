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
| `account` | Read account identity or account-scoped metadata. | `profile`, `whoami` | `sites/tiktok/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `follow`, `like`, `save` | `sites/tiktok/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/tiktok/operations/authentication.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `unfollow` | `sites/tiktok/operations/destructive-actions.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `comment` | `sites/tiktok/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `creator-videos`, `explore`, `following`, `friends`, `live`, `notifications`, `search`, `user` | `sites/tiktok/operations/private-content.md` |
| `write-actions` | Change remote service state. | `unlike`, `unsave` | `sites/tiktok/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
