---
name: opencli-boss
description: Route reviewed Boss website operations through the OpenCLI Web structured execution boundary.
---

# Boss

Catalog site slug: `boss`.
 Known domains: `www.zhipin.com`, `zhipin.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/boss/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/boss/operations/authentication.md` |
| `content` | Read site content and metadata. | `detail` | `sites/boss/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `search` | `sites/boss/operations/discovery.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `invite`, `send` | `sites/boss/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `chatlist`, `chatmsg`, `joblist`, `recommend`, `resume`, `stats` | `sites/boss/operations/private-content.md` |
| `write-actions` | Change remote service state. | `batchgreet`, `exchange`, `greet`, `mark` | `sites/boss/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
