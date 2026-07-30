# Nowcoder: authentication

Open, change, or clear an authenticated browser session.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `login` | `auth_session_change` / `high` | `opencli nowcoder login [--timeout <timeout>] -f json`<br>Open nowcoder login and wait until the browser session is authenticated | `timeout` (int, optional, default=300) | auth=interactive; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
