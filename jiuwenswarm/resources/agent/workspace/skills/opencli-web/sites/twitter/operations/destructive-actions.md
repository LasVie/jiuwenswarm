# Twitter: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `block` | `destructive_or_admin` / `critical` | `opencli twitter block "<username>" -f json`<br>Block a Twitter user | `username` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `delete` | `destructive_or_admin` / `critical` | `opencli twitter delete "<url>" -f json`<br>Delete a specific tweet by URL | `url` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `list-delete` | `destructive_or_admin` / `critical` | `opencli twitter list-delete "<listId>" [--confirm <true\|false>] [--timeout <timeout>] -f json`<br>Delete a Twitter/X list you own after explicit confirmation | `listId` (string, required, positional); `confirm` (boolean, optional, default=False); `timeout` (int, optional, default=300) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `list-remove` | `destructive_or_admin` / `critical` | `opencli twitter list-remove "<listId>" "<username>" -f json`<br>Remove a user from a Twitter/X list you own (toggles via UI; no-op if not currently a member) | `listId` (string, required, positional); `username` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `list-remove-batch` | `destructive_or_admin` / `critical` | `opencli twitter list-remove-batch "<listId>" "<usernames>" [--interval <interval>] [--timeout <timeout>] -f json`<br>Remove multiple users from a Twitter/X list you own from a comma-separated username list | `listId` (string, required, positional); `usernames` (string, required, positional); `interval` (int, optional, default=5); `timeout` (int, optional, default=600) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `unfollow` | `destructive_or_admin` / `critical` | `opencli twitter unfollow "<username>" -f json`<br>Unfollow a Twitter user | `username` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
