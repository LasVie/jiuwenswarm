# Zhihu: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `favorite` | `reversible_remote_write` / `high` | `opencli zhihu favorite "<target>" [--collection "<collection>"] [--collection-id "<collection-id>"] [--execute <true\|false>] -f json`<br>Favorite a Zhihu answer or article into a specific collection | `target` (str, required, positional); `collection` (str, optional); `collection-id` (str, optional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `follow` | `reversible_remote_write` / `high` | `opencli zhihu follow "<target>" [--execute <true\|false>] -f json`<br>Follow a Zhihu user or question | `target` (str, required, positional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `like` | `reversible_remote_write` / `high` | `opencli zhihu like "<target>" [--execute <true\|false>] -f json`<br>Like a Zhihu answer or article | `target` (str, required, positional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
