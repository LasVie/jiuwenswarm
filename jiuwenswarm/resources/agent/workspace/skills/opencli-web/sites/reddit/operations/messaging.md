# Reddit: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comment` | `message_send` / `high` | `opencli reddit comment "<post-id>" "<text>" -f json`<br>Post a comment on a Reddit post | `post-id` (string, required, positional); `text` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `reply` | `message_send` / `high` | `opencli reddit reply "<comment-id>" "<text>" -f json`<br>Reply to a Reddit comment | `comment-id` (string, required, positional); `text` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
