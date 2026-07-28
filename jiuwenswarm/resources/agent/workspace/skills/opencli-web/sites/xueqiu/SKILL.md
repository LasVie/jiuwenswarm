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
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/xueqiu/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/xueqiu/operations/authentication.md` |
| `private-content` | Read content that depends on an authenticated account. | `comments`, `earnings-date`, `feed`, `fund-holdings`, `fund-snapshot`, `groups`, `hot`, `hot-stock`, `kline`, `search`, `stock`, `watchlist` | `sites/xueqiu/operations/private-content.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
