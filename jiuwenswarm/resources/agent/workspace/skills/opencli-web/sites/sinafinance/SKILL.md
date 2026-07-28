---
name: opencli-sinafinance
description: Route reviewed Sinafinance website operations through the OpenCLI Web structured execution boundary.
---

# Sinafinance

Catalog site slug: `sinafinance`.
 Known domains: `app.cj.sina.com.cn`, `finance.sina.com.cn`, `finance.sina.cn`, `suggest3.sinajs.cn`, `hq.sinajs.cn`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `content` | Read site content and metadata. | `stock` | `sites/sinafinance/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `news` | `sites/sinafinance/operations/discovery.md` |
| `private-content` | Read content that depends on an authenticated account. | `rolling-news`, `stock-rank` | `sites/sinafinance/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
