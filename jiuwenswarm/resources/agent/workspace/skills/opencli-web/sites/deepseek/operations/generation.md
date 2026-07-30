# Deepseek: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli deepseek ask "<prompt>" [--timeout <timeout>] [--new <true\|false>] [--model "<instant\|expert\|vision>"] [--think <true\|false>] [--search <true\|false>] [--file "<file>"] -f json`<br>Send a prompt to DeepSeek and get the response | `prompt` (str, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False); `model` (str, optional, default='instant', choices=instant,expert,vision); `think` (boolean, optional, default=False); `search` (boolean, optional, default=False); `file` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli deepseek new -f json`<br>Start a new conversation in DeepSeek | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
