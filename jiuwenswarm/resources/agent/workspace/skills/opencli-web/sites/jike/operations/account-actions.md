# Jike: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `like` | `reversible_remote_write` / `high` | `opencli jike like "<id>" -f json`<br>点赞即刻帖子 | `id` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
