# Doubao: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli doubao ask "<text>" [--timeout <timeout>] -f json`<br>Send a prompt and wait for the Doubao response | `text` (str, required, positional); `timeout` (int, optional, default=60) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli doubao new -f json`<br>Start a new conversation in Doubao web chat | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
