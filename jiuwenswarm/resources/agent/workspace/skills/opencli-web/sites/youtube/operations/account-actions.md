# Youtube: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `like` | `reversible_remote_write` / `high` | `opencli youtube like "<url>" -f json`<br>Like a YouTube video | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `subscribe` | `reversible_remote_write` / `high` | `opencli youtube subscribe "<channel>" -f json`<br>Subscribe to a YouTube channel | `channel` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
