---
name: opencli-yahoo-finance
description: Route reviewed Yahoo Finance website operations through the OpenCLI Web structured execution boundary.
---

# Yahoo Finance

Catalog site slug: `yahoo-finance`.
 Known domains: `finance.yahoo.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `analytics` | Read aggregate metrics, trends, or rankings. | `quote` | `sites/yahoo-finance/operations/analytics.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
