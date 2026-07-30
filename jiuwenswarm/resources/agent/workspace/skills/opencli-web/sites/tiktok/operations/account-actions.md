# Tiktok: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `follow` | `reversible_remote_write` / `high` | `opencli tiktok follow "<username>" -f json`<br>Follow a TikTok user by username | `username` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `like` | `reversible_remote_write` / `high` | `opencli tiktok like "<url>" -f json`<br>Like a TikTok video | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `save` | `reversible_remote_write` / `high` | `opencli tiktok save "<url>" -f json`<br>Add a TikTok video to Favorites | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
