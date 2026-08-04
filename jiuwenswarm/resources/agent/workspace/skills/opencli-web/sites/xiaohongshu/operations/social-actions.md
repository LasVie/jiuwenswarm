# Xiaohongshu: social-actions

Change social relationships or delete published content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `delete-note` | `destructive_or_admin` / `critical` | `opencli xiaohongshu delete-note "<note-id>" [--execute <true\|false>] -f json`<br>删除小红书已发布笔记 (creator center UI automation) | `note-id` (str, required, positional); `execute` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `follow` | `reversible_remote_write` / `high` | `opencli xiaohongshu follow "<full-profile-url>" -f json`<br>关注小红书用户 (profile UI automation) | `user-id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `unfollow` | `destructive_or_admin` / `critical` | `opencli xiaohongshu unfollow "<full-profile-url>" -f json`<br>取消关注小红书用户 (profile UI automation) | `user-id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `follow`: Before asking for confirmation, inspect the original full profile URL read-only with browser_agent and capture both the visible nickname and visible 小红书号. Treat /user/profile/<id> only as an internal profile ID, never as the user-facing 小红书号. If the query delimiter is fullwidth ？, normalize only that delimiter to ? and preserve the rest of the query. Confirm using nickname, 小红书号, and internal profile ID; stop if any identity or target match is uncertain. After confirmation, invoke follow exactly once and stop without retry if the result or visible state is uncertain. Require a separate confirmation before a later unfollow
- `unfollow`: Before asking for confirmation, inspect the original full profile URL read-only with browser_agent and capture both the visible nickname and visible 小红书号. Treat /user/profile/<id> only as an internal profile ID, never as the user-facing 小红书号. Confirm using nickname, 小红书号, and internal profile ID; stop if identity or target match is uncertain. After confirmation, invoke unfollow exactly once. If the command errors, do not retry: inspect the visible profile button read-only and report the command error together with the observed state, without claiming success when the state remains uncertain
