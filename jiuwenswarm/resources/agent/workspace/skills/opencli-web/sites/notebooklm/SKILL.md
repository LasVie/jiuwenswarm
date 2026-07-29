---
name: opencli-notebooklm
description: Route reviewed Notebooklm website operations through the OpenCLI Web structured execution boundary.
---

# Notebooklm

Catalog site slug: `notebooklm`.
 Known domains: `google.com`, `notebooklm.google.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `status`, `whoami` | `sites/notebooklm/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/notebooklm/operations/authentication.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `generate-audio`, `generate-slides` | `sites/notebooklm/operations/generation.md` |
| `private-content` | Read content that depends on an authenticated account. | `current`, `get`, `history`, `list`, `note-list`, `notes-get`, `open`, `source-fulltext`, `source-get`, `source-guide`, `source-list`, `summary` | `sites/notebooklm/operations/private-content.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `create` | `sites/notebooklm/operations/publishing.md` |
| `write-actions` | Change remote service state. | `add-source`, `write-note` | `sites/notebooklm/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
