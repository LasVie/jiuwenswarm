---
name: opencli-douyin
description: Route reviewed Douyin website operations through the OpenCLI Web structured execution boundary.
---

# Douyin

Catalog site slug: `douyin`.
 Known domains: `creator.douyin.com`, `www.douyin.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `profile`, `whoami` | `sites/douyin/operations/account.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/douyin/operations/authentication.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `delete` | `sites/douyin/operations/destructive-actions.md` |
| `private-content` | Read content that depends on an authenticated account. | `activities`, `collections`, `drafts`, `hashtag`, `location`, `search`, `stats`, `user-videos`, `videos` | `sites/douyin/operations/private-content.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `publish`, `update` | `sites/douyin/operations/publishing.md` |
| `write-actions` | Change remote service state. | `draft` | `sites/douyin/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
