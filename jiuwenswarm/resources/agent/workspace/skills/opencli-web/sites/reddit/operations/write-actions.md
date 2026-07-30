# Reddit: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `upvote` | `reversible_remote_write` / `high` | `opencli reddit upvote "<post-id>" [--direction "<direction>"] -f json`<br>Upvote or downvote a Reddit post | `post-id` (string, required, positional); `direction` (string, optional, default='up') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
