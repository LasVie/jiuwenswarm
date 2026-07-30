# Qwen: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `send` | `message_send` / `high` | `opencli qwen send "<prompt>" [--new <true\|false>] [--think <true\|false>] [--research <true\|false>] -f json`<br>Fire-and-forget: send a prompt to Qianwen without waiting for the reply | `prompt` (str, required, positional); `new` (boolean, optional, default=False); `think` (boolean, optional, default=False); `research` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
