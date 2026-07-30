# Hupu: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `like` | `reversible_remote_write` / `high` | `opencli hupu like "<tid>" "<pid>" --fid "<fid>" -f json`<br>点赞虎扑回复 (需要登录) | `tid` (str, required, positional); `pid` (str, required, positional); `fid` (str, required) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
