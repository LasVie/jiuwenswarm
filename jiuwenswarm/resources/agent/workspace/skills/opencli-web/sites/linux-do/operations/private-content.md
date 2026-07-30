# Linux Do: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `private_content_read` / `medium` | `opencli linux-do feed [--view "<latest\|hot\|top>"] [--tag "<tag>"] [--category "<category>"] [--limit <limit>] [--order "<default\|created\|activity\|views\|posts\|category\|likes\|op_likes\|posters>"] [--ascending <true\|false>] [--period "<all\|daily\|weekly\|monthly\|quarterly\|yearly>"] -f json`<br>linux.do 话题列表（需登录；支持全站、标签、分类） | `view` (str, optional, default='latest', choices=latest,hot,top); `tag` (str, optional); `category` (str, optional); `limit` (int, optional, default=20); `order` (str, optional, default='default', choices=default,created,activity,views,posts,category,likes,op_likes,posters); `ascending` (boolean, optional, default=False); `period` (str, optional, choices=all,daily,weekly,monthly,quarterly,yearly) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `feed`: sensitive output: private content, account identifiers
