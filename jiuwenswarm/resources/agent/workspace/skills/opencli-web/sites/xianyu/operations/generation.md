# Xianyu: generation

Generate remote content, start AI work, or consume quota.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `chat` | `quota_consumption` / `high` | `opencli xianyu chat "<item_id>" "<user_id>" [--text "<text>"] -f json`<br>打开闲鱼聊一聊会话，并可选发送消息 | `item_id` (str, required, positional); `user_id` (str, required, positional); `text` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
