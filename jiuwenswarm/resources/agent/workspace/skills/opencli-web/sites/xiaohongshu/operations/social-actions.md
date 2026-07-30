# Xiaohongshu: social-actions

Change social relationships or delete published content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `delete-note` | `destructive_or_admin` / `critical` | `opencli xiaohongshu delete-note "<note-id>" [--execute <true\|false>] -f json`<br>删除小红书已发布笔记 (creator center UI automation) | `note-id` (str, required, positional); `execute` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `follow` | `reversible_remote_write` / `high` | `opencli xiaohongshu follow "<user-id>" -f json`<br>关注小红书用户 (profile UI automation) | `user-id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `unfollow` | `destructive_or_admin` / `critical` | `opencli xiaohongshu unfollow "<user-id>" -f json`<br>取消关注小红书用户 (profile UI automation) | `user-id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
