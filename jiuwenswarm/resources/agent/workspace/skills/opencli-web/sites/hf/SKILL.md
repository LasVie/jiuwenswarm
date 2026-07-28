---
name: opencli-hf
description: Route reviewed Hf website operations through the OpenCLI Web structured execution boundary.
---

# Hf

Catalog site slug: `hf`.
 Known domains: `huggingface.co`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/hf/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/hf/operations/authentication.md` |
| `content` | Read site content and metadata. | `datasets`, `models`, `paper`, `spaces`, `top` | `sites/hf/operations/content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
