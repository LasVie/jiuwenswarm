# Deepseek: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `send` | `message_send` / `high` | `opencli deepseek send "<id>" "<prompt>" [--timeout <timeout>] -f json`<br>Send a prompt to a specific DeepSeek conversation by ID, without waiting for a response | `id` (str, required, positional); `prompt` (str, required, positional); `timeout` (int, optional, default=60) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
