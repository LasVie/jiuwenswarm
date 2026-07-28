---
name: opencli-hupu
description: Route reviewed Hupu website operations through the OpenCLI Web structured execution boundary.
---

# Hupu

Catalog site slug: `hupu`.
 Known domains: `bbs.hupu.com`, `hupu.com`, `my.hupu.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/hupu/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `like` | `sites/hupu/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/hupu/operations/authentication.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `reply` | `sites/hupu/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `detail`, `hot`, `mentions`, `search` | `sites/hupu/operations/private-content.md` |
| `write-actions` | Change remote service state. | `unlike` | `sites/hupu/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
