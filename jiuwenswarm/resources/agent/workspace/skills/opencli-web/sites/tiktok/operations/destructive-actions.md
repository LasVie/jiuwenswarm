# Tiktok: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `unfollow` | `destructive_or_admin` / `critical` | `opencli tiktok unfollow "<username>" -f json`<br>Unfollow a TikTok user by username | `username` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
