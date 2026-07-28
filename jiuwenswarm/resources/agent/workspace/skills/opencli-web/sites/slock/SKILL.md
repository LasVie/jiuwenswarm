---
name: opencli-slock
description: Route reviewed Slock website operations through the OpenCLI Web structured execution boundary.
---

# Slock

Catalog site slug: `slock`.
 Known domains: `app.slock.ai`.

Read this file only through the main Agent's SkillTool. Do not delegate disclosure to a general-purpose or browser subagent and do not replace it with a filesystem read.

## Capability groups

This file is a router, not an execution receipt. Select exactly one operation and read its full path again with SkillTool from the same main Agent.

| Operation | Purpose | Commands | Terminal contract path |
|---|---|---|---|
| `account` | Read account identity or account-scoped metadata. | `whoami` | `sites/slock/operations/account.md` |
| `account-actions` | Change reversible account relationship or saved state. | `bookmark-add`, `thread-follow` | `sites/slock/operations/account-actions.md` |
| `authentication` | Open, change, or clear an authenticated browser session. | `login` | `sites/slock/operations/authentication.md` |
| `destructive-actions` | Delete, remove, revoke, or perform administrative changes. | `bookmark-remove`, `reaction-remove`, `task-delete`, `thread-unfollow` | `sites/slock/operations/destructive-actions.md` |
| `file-operations` | Create or download workspace files. | `attachment-download`, `channel-archive` | `sites/slock/operations/file-operations.md` |
| `messaging` | Send messages, replies, comments, invitations, or contacts. | `message-send` | `sites/slock/operations/messaging.md` |
| `private-content` | Read content that depends on an authenticated account. | `attachment-url`, `bookmark-list`, `channel-files`, `channel-info`, `channel-list`, `channel-members`, `dm-list`, `inbox`, `message-read`, `message-search`, `server-list`, `task-get`, `task-list`, `task-list-server`, `thread-list`, `unread-summary` | `sites/slock/operations/private-content.md` |
| `publishing` | Publish, create, edit, or upload remote content. | `attachment-upload`, `channel-create`, `task-create` | `sites/slock/operations/publishing.md` |
| `write-actions` | Change remote service state. | `channel-join`, `channel-leave`, `channel-mark`, `channel-unarchive`, `inbox-done`, `inbox-read-all`, `reaction-add`, `server-use`, `task-claim`, `task-convert`, `task-status`, `task-unclaim`, `thread-done`, `thread-undone` | `sites/slock/operations/write-actions.md` |

Do not skip the operation read. Optional references can explain examples or output shape, but they never authorize execution.
