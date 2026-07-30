# Hupu: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `unlike` | `reversible_remote_write` / `high` | `opencli hupu unlike "<tid>" "<pid>" --fid "<fid>" -f json`<br>取消点赞虎扑回复 (需要登录) | `tid` (str, required, positional); `pid` (str, required, positional); `fid` (str, required) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
