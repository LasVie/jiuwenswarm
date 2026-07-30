# Doubao: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `send` | `message_send` / `high` | `opencli doubao send "<text>" -f json`<br>Send a message to Doubao web chat | `text` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
