# Facebook: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `add-friend` | `reversible_remote_write` / `high` | `opencli facebook add-friend "<username>" -f json`<br>Send a friend request on Facebook | `username` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `join-group` | `reversible_remote_write` / `high` | `opencli facebook join-group "<group>" -f json`<br>Join a Facebook group | `group` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
