# Douyin: destructive-actions

Delete, remove, revoke, or perform administrative changes.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `delete` | `destructive_or_admin` / `critical` | `opencli douyin delete "<aweme_id>" -f json`<br>删除作品（优先使用创作者后台作品管理；找不到时回退到旧删除接口） | `aweme_id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
