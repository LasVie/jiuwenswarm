# Midjourney: authentication

Open, change, or clear an authenticated browser session.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `login` | `auth_session_change` / `high` | `opencli midjourney login [--timeout <timeout>] -f json`<br>Open Midjourney in a foreground Chrome window and wait for login to complete | `timeout` (int, optional, default=300) | auth=interactive; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
