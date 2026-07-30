# Slock: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `message-send` | `message_send` / `high` | `opencli slock message-send "<target>" "<content>" [--dry-run <true\|false>] [--as-task <true\|false>] [--attach "<attach>"] [--server "<server>"] -f json`<br>Send a message to a channel, DM, or thread (content sent verbatim) | `target` (str, required, positional); `content` (str, required, positional); `dry-run` (bool, optional, default=False); `as-task` (bool, optional, default=False); `attach` (str, optional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
