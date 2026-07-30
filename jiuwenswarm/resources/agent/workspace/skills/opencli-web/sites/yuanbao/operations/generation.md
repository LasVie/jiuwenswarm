# Yuanbao: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli yuanbao ask "<prompt>" [--timeout <timeout>] [--search <true\|false>] [--think <true\|false>] -f json`<br>Send a prompt to Yuanbao web chat and wait for the assistant response | `prompt` (str, required, positional); `timeout` (int, optional, default=60); `search` (boolean, optional, default=True); `think` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli yuanbao new -f json`<br>Start a new conversation in Yuanbao web chat | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
