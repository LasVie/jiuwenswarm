# Xianyu: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `inbox` | `private_content_read` / `medium` | `opencli xianyu inbox [--limit <limit>] [--unread-only <true\|false>] [--resolve-ids <true\|false>] -f json`<br>列出闲鱼最近私信会话 | `limit` (int, optional, default=20); `unread-only` (bool, optional, default=False); `resolve-ids` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `messages` | `private_content_read` / `medium` | `opencli xianyu messages ["<item_id>"] ["<user_id>"] [--limit <limit>] [--rank <rank>] -f json`<br>读取指定闲鱼私信会话的最近聊天内容 | `item_id` (str, optional, positional); `user_id` (str, optional, positional); `limit` (int, optional, default=50); `rank` (int, optional, default=0) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `inbox`: sensitive output: private content, account identifiers
- `messages`: sensitive output: private content, account identifiers
