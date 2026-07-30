# Kimi: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli kimi ask "<text>" [--timeout <timeout>] -f json`<br>Send a message and wait up to --timeout seconds for the assistant reply (best-effort: polls for turn count to grow + stabilize). | `text` (str, required, positional); `timeout` (int, optional, default=120) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli kimi new -f json`<br>Start a new Kimi chat (navigates to / with chat_enter_method=new_chat). | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
