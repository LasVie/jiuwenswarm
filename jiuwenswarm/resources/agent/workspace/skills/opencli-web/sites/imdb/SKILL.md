---
name: opencli-imdb
description: Route reviewed Imdb website operations through the OpenCLI Web structured execution boundary.
---

# Imdb

Catalog site slug: `imdb`.
 Known domains: `www.imdb.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `private-content` | Read content that depends on an authenticated account. | `person`, `reviews`, `search`, `title`, `top`, `trending` | `sites/imdb/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
