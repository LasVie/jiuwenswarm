# Slock: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `bookmark-remove` | `destructive_or_admin` / `critical` | `opencli slock bookmark-remove "<messageId>" [--server "<server>"] -f json`<br>Remove a bookmark (DELETE /channels/saved/:messageId). 404 is treated as already-removed. | `messageId` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `reaction-remove` | `destructive_or_admin` / `critical` | `opencli slock reaction-remove "<messageId>" "<emoji>" [--server "<server>"] -f json`<br>Remove your emoji reaction from a message (DELETE /messages/:id/reactions). | `messageId` (str, required, positional); `emoji` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `task-delete` | `destructive_or_admin` / `critical` | `opencli slock task-delete "<taskId>" [--confirm <true\|false>] [--server "<server>"] -f json`<br>Delete a chat task (DELETE /tasks/:taskId). Requires --confirm — destructive, irreversible. | `taskId` (str, required, positional); `confirm` (bool, optional, default=False); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `thread-unfollow` | `destructive_or_admin` / `critical` | `opencli slock thread-unfollow "<threadChannelId>" [--server "<server>"] -f json`<br>Stop following a thread (POST /channels/threads/unfollow) | `threadChannelId` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
