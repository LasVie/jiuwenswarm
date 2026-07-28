---
name: opencli-chatgpt
description: Route reviewed Chatgpt website operations through the OpenCLI Web structured execution boundary.
---

# Chatgpt

Catalog site slug: `chatgpt`.
 Known domains: `chatgpt.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/chatgpt/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/chatgpt/operations/authentication.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `ask`, `deep-research-result`, `image`, `new` | `sites/chatgpt/operations/generation.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `send` | `sites/chatgpt/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `detail`, `history`, `project-list`, `read`, `status` | `sites/chatgpt/operations/private-content.md` |
| `write-actions` | Change remote service state. | `model`, `project-file-add` | `sites/chatgpt/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
