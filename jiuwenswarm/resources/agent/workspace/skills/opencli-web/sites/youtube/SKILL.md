---
name: opencli-youtube
description: Route reviewed Youtube website operations through the OpenCLI Web structured execution boundary.
---

# Youtube

Catalog site slug: `youtube`.
 Known domains: `www.youtube.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/youtube/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `like`, `subscribe` | `sites/youtube/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/youtube/operations/authentication.md` |
| `content` | Read one public item, record, page, or resource. | `channel`, `comments`, `transcript`, `video` | `sites/youtube/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search` | `sites/youtube/operations/discovery.md` |
| `private-content` | Read content that depends on an authenticated account. | `feed`, `history`, `playlist`, `subscriptions`, `watch-later` | `sites/youtube/operations/private-content.md` |
| `write-actions` | Change remote service state. | `unlike`, `unsubscribe` | `sites/youtube/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
