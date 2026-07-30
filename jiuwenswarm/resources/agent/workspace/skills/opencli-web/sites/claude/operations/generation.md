# Claude: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `quota_consumption` / `high` | `opencli claude ask "<prompt>" [--timeout <timeout>] [--new <true\|false>] [--model "<sonnet\|opus\|haiku>"] [--think <true\|false>] [--file "<file>"] -f json`<br>Send a prompt to Claude and get the response | `prompt` (str, required, positional); `timeout` (int, optional, default=120); `new` (boolean, optional, default=False); `model` (str, optional, default='sonnet', choices=sonnet,opus,haiku); `think` (boolean, optional, default=False); `file` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `new` | `quota_consumption` / `high` | `opencli claude new -f json`<br>Start a new conversation in Claude | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
