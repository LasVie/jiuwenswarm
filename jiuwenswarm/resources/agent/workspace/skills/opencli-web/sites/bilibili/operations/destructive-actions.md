# Bilibili: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `unfollow` | `destructive_or_admin` / `critical` | `opencli bilibili unfollow "<target>" -f json`<br>取消关注 B站用户（官方 API，需登录） | `target` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
