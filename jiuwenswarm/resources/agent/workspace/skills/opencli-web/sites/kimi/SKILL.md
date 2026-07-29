---
name: opencli-kimi
description: Route reviewed Kimi website operations through the OpenCLI Web structured execution boundary.
---

# Kimi

Catalog site slug: `kimi`.
 Known domains: `kimi.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `account`, `cookies`, `idb-list`, `status`, `storage-get`, `storage-keys`, `usage`, `whoami` | `sites/kimi/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/kimi/operations/authentication.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `templates` | `sites/kimi/operations/discovery.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `ask`, `new` | `sites/kimi/operations/generation.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `copy-message`, `send` | `sites/kimi/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `detail`, `history`, `read` | `sites/kimi/operations/private-content.md` |
| `write-actions` | Change remote service state. | `dismiss-banner`, `history-rename`, `mode`, `model`, `react`, `regenerate`, `settings`, `share`, `sidebar-toggle`, `sign-out`, `upgrade`, `view-all-history` | `sites/kimi/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
