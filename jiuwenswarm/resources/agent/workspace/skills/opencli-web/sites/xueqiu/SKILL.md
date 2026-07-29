---
name: opencli-xueqiu
description: Route reviewed Xueqiu website operations through the OpenCLI Web structured execution boundary.
---

# Xueqiu

Catalog site slug: `xueqiu`.
 Known domains: `danjuanfunds.com`, `xueqiu.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `fund-holdings`, `fund-snapshot`, `groups`, `watchlist`, `whoami` | `sites/xueqiu/operations/account.md` |
| `analytics` | Read aggregate metrics, trends, or rankings. | `earnings-date`, `kline`, `stock` | `sites/xueqiu/operations/analytics.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/xueqiu/operations/authentication.md` |
| `content` | Read site content and metadata. | `comments` | `sites/xueqiu/operations/content.md` |
| `discovery` | Search, browse, recommend, or discover site content. | `hot`, `hot-stock`, `search` | `sites/xueqiu/operations/discovery.md` |
| `private-content` | Read content that depends on an authenticated account. | `feed` | `sites/xueqiu/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
