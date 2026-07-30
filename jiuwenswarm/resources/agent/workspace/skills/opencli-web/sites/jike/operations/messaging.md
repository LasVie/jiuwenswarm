# Jike: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comment` | `message_send` / `high` | `opencli jike comment "<id>" "<text>" -f json`<br>评论即刻帖子 | `id` (string, required, positional); `text` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |
