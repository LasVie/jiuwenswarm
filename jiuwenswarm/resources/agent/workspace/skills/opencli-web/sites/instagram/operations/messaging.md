# Instagram: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comment` | `message_send` / `high` | `opencli instagram comment "<username>" "<text>" [--index <index>] -f json`<br>Comment on an Instagram post | `username` (str, required, positional); `text` (str, required, positional); `index` (int, optional, default=1) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
