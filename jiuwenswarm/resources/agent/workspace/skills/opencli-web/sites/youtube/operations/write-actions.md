# Youtube: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `unlike` | `reversible_remote_write` / `high` | `opencli youtube unlike "<url>" -f json`<br>Remove like from a YouTube video | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `unsubscribe` | `reversible_remote_write` / `high` | `opencli youtube unsubscribe "<channel>" -f json`<br>Unsubscribe from a YouTube channel | `channel` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
