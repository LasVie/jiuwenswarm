# Twitter: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `bookmark` | `reversible_remote_write` / `high` | `opencli twitter bookmark "<url>" -f json`<br>Bookmark a tweet | `url` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `follow` | `reversible_remote_write` / `high` | `opencli twitter follow "<username>" -f json`<br>Follow a Twitter user | `username` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `follow-batch` | `reversible_remote_write` / `high` | `opencli twitter follow-batch "<usernames>" [--delay-ms <delay-ms>] -f json`<br>Follow multiple Twitter/X users from a comma-separated username list | `usernames` (string, required, positional); `delay-ms` (int, optional, default=3000) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
| `like` | `reversible_remote_write` / `high` | `opencli twitter like "<url>" -f json`<br>Like a specific tweet | `url` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
