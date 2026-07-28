---
name: opencli-yollomi
description: Route reviewed Yollomi website operations through the OpenCLI Web structured execution boundary.
---

# Yollomi

Catalog site slug: `yollomi`.
 Known domains: `yollomi.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `content` | Read site content and metadata. | `models` | `sites/yollomi/operations/content.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `remove-bg` | `sites/yollomi/operations/destructive-actions.md` |
| `generation` | Generate remote content, start AI work, or consume quota. | `generate` | `sites/yollomi/operations/generation.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `edit`, `upload` | `sites/yollomi/operations/publishing.md` |
| `write-actions` | Change remote service state. | `background`, `face-swap`, `object-remover`, `restore`, `try-on`, `upscale`, `video` | `sites/yollomi/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
