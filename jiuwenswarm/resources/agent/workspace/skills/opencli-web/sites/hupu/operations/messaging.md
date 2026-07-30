# Hupu: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `reply` | `message_send` / `high` | `opencli hupu reply "<tid>" --topic_id "<topic_id>" "<text>" [--quote_id "<quote_id>"] -f json`<br>回复虎扑帖子 (需要登录) | `tid` (str, required, positional); `topic_id` (str, required); `text` (str, required, positional); `quote_id` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
