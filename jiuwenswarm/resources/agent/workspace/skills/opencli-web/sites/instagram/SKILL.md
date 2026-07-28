---
name: opencli-instagram
description: Route reviewed Instagram website operations through the OpenCLI Web structured execution boundary.
---

# Instagram

Catalog site slug: `instagram`.
 Known domains: `instagram.com`, `www.instagram.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `profile`, `whoami` | `sites/instagram/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `follow`, `like`, `save` | `sites/instagram/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/instagram/operations/authentication.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `collection-delete`, `unfollow` | `sites/instagram/operations/destructive-actions.md` |
| `file-operations` | Create or download workspace files. | `download` | `sites/instagram/operations/file-operations.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `comment` | `sites/instagram/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `explore`, `followers`, `following`, `saved`, `search`, `user` | `sites/instagram/operations/private-content.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `collection-create`, `post` | `sites/instagram/operations/publishing.md` |
| `write-actions` | Change remote service state. | `note`, `reel`, `story`, `unlike`, `unsave` | `sites/instagram/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
