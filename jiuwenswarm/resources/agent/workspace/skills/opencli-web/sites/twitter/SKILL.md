---
name: opencli-twitter
description: Route reviewed Twitter website operations through the OpenCLI Web structured execution boundary.
---

# Twitter

Catalog site slug: `twitter`.
 Known domains: `x.com`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `profile`, `whoami` | `sites/twitter/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `bookmark`, `follow`, `follow-batch`, `like` | `sites/twitter/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/twitter/operations/authentication.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `block`, `delete`, `list-delete`, `list-remove`, `list-remove-batch`, `unfollow` | `sites/twitter/operations/destructive-actions.md` |
| `file-operations` | Create or download workspace files. | `download` | `sites/twitter/operations/file-operations.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `hide-reply`, `reply`, `reply-dm` | `sites/twitter/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `article`, `bookmark-folder`, `bookmark-folders`, `bookmarks`, `device-follow`, `followers`, `following`, `likes`, `list-tweets`, `lists`, `notifications`, `search`, `thread`, `timeline`, `trending`, `tweets` | `sites/twitter/operations/private-content.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `list-create`, `post` | `sites/twitter/operations/publishing.md` |
| `write-actions` | Change remote service state. | `accept`, `list-add`, `list-add-batch`, `quote`, `retweet`, `unblock`, `unbookmark`, `unlike`, `unretweet` | `sites/twitter/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
