---
name: opencli-google
description: Route reviewed Google website operations through the OpenCLI Web structured execution boundary.
---

# Google

Catalog site slug: `google`.
 Known domains: `google.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `news`, `suggest`, `trends` | `sites/google/operations/public-data.md` |
| `web-search` | Read browser-rendered web search results. | `search` | `sites/google/operations/web-search.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
