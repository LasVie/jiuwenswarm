# Qwen: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli qwen ask "<prompt>" [--timeout <timeout>] [--new <true\|false>] [--think <true\|false>] [--research <true\|false>] [--markdown <true\|false>] -f json`<br>Send a prompt to Qianwen and return the assistant reply | `prompt` (str, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False); `think` (boolean, optional, default=False); `research` (boolean, optional, default=False); `markdown` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `image` | `quota_consumption` / `high` | `opencli qwen image "<prompt>" [--op "<op>"] [--new <true\|false>] [--sd <true\|false>] [--timeout <timeout>] -f json`<br>Generate images with Qianwen (AI生图) and save them locally | `prompt` (str, required, positional); `op` (str, optional, default='~/Pictures/qianwen'); `new` (boolean, optional, default=True); `sd` (boolean, optional, default=False); `timeout` (int, optional, default=180) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli qwen new -f json`<br>Start a new conversation in Qianwen | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
