# Instagram: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `collection-delete` | `destructive_or_admin` / `critical` | `opencli instagram collection-delete "<target>" -f json`<br>Delete an Instagram saved-posts collection (folder) by name or id | `target` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `unfollow` | `destructive_or_admin` / `critical` | `opencli instagram unfollow "<username>" -f json`<br>Unfollow an Instagram user | `username` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
