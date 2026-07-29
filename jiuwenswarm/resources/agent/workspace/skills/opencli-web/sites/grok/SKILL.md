---
name: opencli-grok
description: Route reviewed Grok website operations through the OpenCLI Web structured execution boundary.
---

# Grok

Catalog site slug: `grok`.
 Known domains: `grok.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `status`, `whoami` | `sites/grok/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `pin` | `sites/grok/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/grok/operations/authentication.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `delete` | `sites/grok/operations/destructive-actions.md` |
| `file-operations` | Create or download workspace files. | `export-all` | `sites/grok/operations/file-operations.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `ask`, `image`, `new` | `sites/grok/operations/generation.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `send` | `sites/grok/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `detail`, `export`, `history`, `read` | `sites/grok/operations/private-content.md` |
| `write-actions` | Change remote service state. | `unpin` | `sites/grok/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
