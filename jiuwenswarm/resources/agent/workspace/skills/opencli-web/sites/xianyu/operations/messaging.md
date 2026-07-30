# Xianyu: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `reply` | `message_send` / `high` | `opencli xianyu reply ["<item_id>"] ["<user_id>"] --text "<text>" [--rank <rank>] -f json`<br>回复指定闲鱼私信会话 | `item_id` (str, optional, positional); `user_id` (str, optional, positional); `text` (str, required); `rank` (int, optional, default=0) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
