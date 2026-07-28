---
name: opencli-qwen
description: Route reviewed Qwen website operations through the OpenCLI Web structured execution boundary.
---

# Qwen

Catalog site slug: `qwen`.
 Known domains: `qwen.ai`, `www.qianwen.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/qwen/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/qwen/operations/authentication.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `ask`, `image`, `new` | `sites/qwen/operations/generation.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `send` | `sites/qwen/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `detail`, `history`, `read`, `status` | `sites/qwen/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
