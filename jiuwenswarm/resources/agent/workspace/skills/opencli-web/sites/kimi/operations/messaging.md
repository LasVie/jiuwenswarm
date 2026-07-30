# Kimi: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `copy-message` | `message_send` / `high` | `opencli kimi copy-message [--conv "<conv>"] [--click-button <true\|false>] -f json`<br>Return the text of the last assistant message. Pass --conv <id> to navigate to a specific chat first. | `conv` (str, optional); `click-button` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `send` | `message_send` / `high` | `opencli kimi send "<text>" -f json`<br>Send a message in the current Kimi chat (fire-and-forget; does not wait for reply). | `text` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
