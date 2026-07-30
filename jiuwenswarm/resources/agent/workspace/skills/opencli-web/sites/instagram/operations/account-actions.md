# Instagram: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `follow` | `reversible_remote_write` / `high` | `opencli instagram follow "<username>" -f json`<br>Follow an Instagram user | `username` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `like` | `reversible_remote_write` / `high` | `opencli instagram like "<username>" [--index <index>] -f json`<br>Like an Instagram post | `username` (str, required, positional); `index` (int, optional, default=1) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `save` | `reversible_remote_write` / `high` | `opencli instagram save "<username>" [--index <index>] -f json`<br>Save (bookmark) an Instagram post | `username` (str, required, positional); `index` (int, optional, default=1) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
