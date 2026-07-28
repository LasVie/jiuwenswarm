---
name: opencli-eastmoney
description: Route reviewed Eastmoney website operations through the OpenCLI Web structured execution boundary.
---

# Eastmoney

Catalog site slug: `eastmoney`.
 Known domains: `datacenter-web.eastmoney.com`, `guba.eastmoney.com`, `np-anotice-stock.eastmoney.com`, `np-listapi.eastmoney.com`, `push2.eastmoney.com`, `push2his.eastmoney.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `content` | Read site content and metadata. | `announcement`, `convertible`, `etf`, `holders`, `index-board`, `kline`, `kuaixun`, `longhu`, `money-flow`, `northbound`, `quote`, `rank`, `sectors` | `sites/eastmoney/operations/content.md` |
| `private-content` | Read content that depends on an authenticated account. | `hot-rank` | `sites/eastmoney/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
