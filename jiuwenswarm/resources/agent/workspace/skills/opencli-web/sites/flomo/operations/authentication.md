# Flomo: authentication

Open, change, or clear an authenticated browser session.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `login` | `auth_session_change` / `high` | `opencli flomo login [--timeout <timeout>] -f json`<br>Open flomo login and wait until the browser session is authenticated | `timeout` (int, optional, default=300, minimum=1,maximum=1800) | auth=interactive; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
