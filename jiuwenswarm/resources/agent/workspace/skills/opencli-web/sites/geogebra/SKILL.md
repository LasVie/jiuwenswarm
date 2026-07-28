---
name: opencli-geogebra
description: Route reviewed Geogebra website operations through the OpenCLI Web structured execution boundary.
---

# Geogebra

Catalog site slug: `geogebra`.
 Known domains: `www.geogebra.org`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `arbitrary-execution` | Adapter entry points that can execute arbitrary input. | `eval` | `sites/geogebra/operations/arbitrary-execution.md` |
| `private-content` | Read content that depends on an authenticated account. | `info`, `list` | `sites/geogebra/operations/private-content.md` |
| `write-actions` | Change remote service state. | `add-circle`, `add-line`, `add-point`, `add-polygon`, `hexagon`, `triangle` | `sites/geogebra/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
