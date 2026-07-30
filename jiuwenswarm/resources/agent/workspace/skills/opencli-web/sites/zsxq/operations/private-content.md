# Zsxq: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `dynamics` | `private_content_read` / `medium` | `opencli zsxq dynamics [--limit <limit>] -f json`<br>获取所有星球的最新动态 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `groups` | `private_content_read` / `medium` | `opencli zsxq groups [--limit <limit>] -f json`<br>列出当前账号加入的星球 | `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `private_content_read` / `medium` | `opencli zsxq search "<keyword>" [--limit <limit>] [--group_id "<group_id>"] -f json`<br>搜索星球内容 | `keyword` (str, required, positional); `limit` (int, optional, default=20); `group_id` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `topic` | `private_content_read` / `medium` | `opencli zsxq topic "<id>" [--group_id "<group_id>"] [--comment_limit <comment_limit>] -f json`<br>获取单个话题详情和评论 | `id` (str, required, positional); `group_id` (str, optional); `comment_limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `topics` | `private_content_read` / `medium` | `opencli zsxq topics [--limit <limit>] [--group_id "<group_id>"] -f json`<br>获取当前星球的话题列表 | `limit` (int, optional, default=20); `group_id` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `dynamics`: sensitive output: private content, account identifiers
- `groups`: sensitive output: private content, account identifiers
- `search`: sensitive output: private content, account identifiers
- `topic`: sensitive output: private content, account identifiers
- `topics`: sensitive output: private content, account identifiers
