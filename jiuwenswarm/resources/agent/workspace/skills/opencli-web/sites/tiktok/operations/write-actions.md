# Tiktok: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `unlike` | `reversible_remote_write` / `high` | `opencli tiktok unlike "<url>" -f json`<br>Unlike a TikTok video | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `unsave` | `reversible_remote_write` / `high` | `opencli tiktok unsave "<url>" -f json`<br>Remove a TikTok video from Favorites | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
