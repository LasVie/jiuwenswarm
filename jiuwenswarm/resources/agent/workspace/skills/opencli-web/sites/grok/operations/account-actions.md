# Grok: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `pin` | `reversible_remote_write` / `high` | `opencli grok pin "<id>" -f json`<br>Pin a Grok conversation by ID | `id` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
