# Bilibili: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `follow` | `reversible_remote_write` / `high` | `opencli bilibili follow "<target>" -f json`<br>关注 B站用户（官方 API，需登录） | `target` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
