# Bilibili: messaging

Send messages, replies, comments, invitations, or contacts.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comment` | `message_send` / `high` | `opencli bilibili comment "<bvid>" "<message>" [--parent <parent>] [--execute <true\|false>] -f json`<br>在 B站视频下发表评论或回复（官方 API，需登录；消息里的 @用户 会被解析为真实提及） | `bvid` (str, required, positional); `message` (str, required, positional); `parent` (int, optional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
