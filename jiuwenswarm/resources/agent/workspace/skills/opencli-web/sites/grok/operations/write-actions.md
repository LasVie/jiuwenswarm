# Grok: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `unpin` | `reversible_remote_write` / `high` | `opencli grok unpin "<id>" -f json`<br>Unpin a Grok conversation by ID | `id` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
