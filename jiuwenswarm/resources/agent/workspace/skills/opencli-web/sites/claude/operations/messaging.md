# Claude: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `send` | `message_send` / `high` | `opencli claude send "<prompt>" [--new <true\|false>] -f json`<br>Send a prompt to Claude without waiting for the response | `prompt` (str, required, positional); `new` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
