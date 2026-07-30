# Boss: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `invite` | `message_send` / `high` | `opencli boss invite "<uid>" --time "<time>" [--address "<address>"] [--contact "<contact>"] -f json`<br>BOSS直聘发送面试邀请 | `uid` (str, required, positional); `time` (str, required); `address` (str, optional, default=''); `contact` (str, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `send` | `message_send` / `high` | `opencli boss send "<uid>" "<text>" -f json`<br>BOSS直聘发送聊天消息 | `uid` (str, required, positional); `text` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
