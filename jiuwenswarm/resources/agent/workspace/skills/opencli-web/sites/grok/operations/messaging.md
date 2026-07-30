# Grok: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `send` | `message_send` / `high` | `opencli grok send "<prompt>" [--new <true\|false>] -f json`<br>Fire-and-forget: send a prompt to Grok without waiting for the reply | `prompt` (str, required, positional); `new` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
