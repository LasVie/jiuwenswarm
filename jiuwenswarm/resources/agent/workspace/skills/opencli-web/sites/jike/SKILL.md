---
name: opencli-jike
description: Route reviewed Jike website operations through the OpenCLI Web structured execution boundary.
---

# Jike

Catalog site slug: `jike`.
 Known domains: `m.okjike.com`, `web.okjike.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/jike/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `like` | `sites/jike/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/jike/operations/authentication.md` |
| `content` | Read one public item, record, page, or resource. | `post`, `topic`, `user` | `sites/jike/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search` | `sites/jike/operations/discovery.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `comment` | `sites/jike/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `feed`, `notifications` | `sites/jike/operations/private-content.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `create` | `sites/jike/operations/publishing.md` |
| `write-actions` | Change remote service state. | `repost` | `sites/jike/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
