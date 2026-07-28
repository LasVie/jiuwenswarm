---
name: opencli-paperreview
description: Route reviewed Paperreview website operations through the OpenCLI Web structured execution boundary.
---

# Paperreview

Catalog site slug: `paperreview`.
 Known domains: `paperreview.ai`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `content` | Read site content and metadata. | `review` | `sites/paperreview/operations/content.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `submit` | `sites/paperreview/operations/publishing.md` |
| `write-actions` | Change remote service state. | `feedback` | `sites/paperreview/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
