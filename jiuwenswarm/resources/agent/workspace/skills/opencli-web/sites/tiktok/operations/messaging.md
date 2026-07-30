# Tiktok: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comment` | `message_send` / `high` | `opencli tiktok comment "<url>" "<text>" -f json`<br>Post a comment on a TikTok video | `url` (str, required, positional); `text` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
