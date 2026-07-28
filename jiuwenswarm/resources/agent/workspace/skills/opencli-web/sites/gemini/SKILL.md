---
name: opencli-gemini
description: Route reviewed Gemini website operations through the OpenCLI Web structured execution boundary.
---

# Gemini

Catalog site slug: `gemini`.
 Known domains: `gemini.google.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/gemini/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/gemini/operations/authentication.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `ask`, `deep-research`, `deep-research-result`, `image`, `new` | `sites/gemini/operations/generation.md` |
| `private-content` | Read content that depends on an authenticated account. | `detail`, `history`, `models`, `read`, `status` | `sites/gemini/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
