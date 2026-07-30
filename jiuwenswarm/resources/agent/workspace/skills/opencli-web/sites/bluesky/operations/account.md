# Bluesky: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `profile` | `public_read` / `low` | `opencli bluesky profile "<handle>" -f json`<br>Get Bluesky user profile info | `handle` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
