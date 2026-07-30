# Spotify: authentication

Open, change, or clear an authenticated browser session.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `auth` | `auth_session_change` / `high` | `opencli spotify auth -f json`<br>Authenticate with Spotify (OAuth — run once) | none | auth=interactive; transport=public_http; fallback_before=browser_agent; fallback_after=none |
