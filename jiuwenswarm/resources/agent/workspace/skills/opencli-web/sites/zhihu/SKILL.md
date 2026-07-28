---
name: opencli-zhihu
description: Route reviewed Zhihu website operations through the OpenCLI Web structured execution boundary.
---

# Zhihu

Catalog site slug: `zhihu`.
 Known domains: `www.zhihu.com`, `zhihu.com`, `zhuanlan.zhihu.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/zhihu/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `favorite`, `follow`, `like` | `sites/zhihu/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/zhihu/operations/authentication.md` |
| `file-operations` | Create or download workspace files. | `download` | `sites/zhihu/operations/file-operations.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `comment` | `sites/zhihu/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `answer-comments`, `answer-detail`, `collection`, `collections`, `followers`, `following`, `hot`, `pins`, `question`, `recommend`, `search`, `user`, `user-answers`, `user-articles` | `sites/zhihu/operations/private-content.md` |
| `write-actions` | Change remote service state. | `answer` | `sites/zhihu/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
