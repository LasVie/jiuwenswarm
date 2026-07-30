# Reddit: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `save` | `reversible_remote_write` / `high` | `opencli reddit save "<post-id>" [--undo <true\|false>] -f json`<br>Save or unsave a Reddit post | `post-id` (string, required, positional); `undo` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `subscribe` | `reversible_remote_write` / `high` | `opencli reddit subscribe "<subreddit>" [--undo <true\|false>] -f json`<br>Subscribe or unsubscribe to a subreddit | `subreddit` (string, required, positional); `undo` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
