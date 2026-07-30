# Ones: authentication

Open, change, or clear an authenticated browser session.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `login` | `auth_session_change` / `high` | `opencli ones login [--email "<email>"] [--phone "<phone>"] [--password "<password>"] -f json`<br>ONES Project API — login via Chrome Bridge (POST auth/login); stderr prints export hints for ONES_USER_ID / TOKEN | `email` (str, optional); `phone` (str, optional); `password` (str, optional) | auth=interactive; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `logout` | `auth_session_change` / `high` | `opencli ones logout -f json`<br>ONES Project API — invalidate current token (GET auth/logout) via Chrome Bridge | none | auth=interactive; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
