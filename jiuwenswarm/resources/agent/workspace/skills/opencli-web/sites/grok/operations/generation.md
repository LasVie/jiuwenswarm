# Grok: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli grok ask "<prompt>" [--timeout <timeout>] [--new <true\|false>] -f json`<br>Send a message to Grok and get response | `prompt` (string, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `image` | `quota_consumption` / `high` | `opencli grok image "<prompt>" [--timeout <timeout>] [--new <true\|false>] [--count <count>] [--out "<out>"] -f json`<br>Generate images on grok.com and return image URLs | `prompt` (string, required, positional); `timeout` (int, optional, default=240); `new` (boolean, optional, default=False); `count` (int, optional, default=1); `out` (string, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli grok new -f json`<br>Start a new conversation in Grok | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
