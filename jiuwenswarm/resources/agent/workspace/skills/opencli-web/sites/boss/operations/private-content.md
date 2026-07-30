# Boss: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `chatlist` | `private_content_read` / `medium` | `opencli boss chatlist [--page <page>] [--limit <limit>] [--job-id "<job-id>"] [--side "<auto\|boss\|geek>"] -f json`<br>BOSS直聘查看聊天列表（招聘端/求职端） | `page` (int, optional, default=1); `limit` (int, optional, default=20); `job-id` (str, optional, default='0'); `side` (str, optional, default='auto', choices=auto,boss,geek) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `chatmsg` | `private_content_read` / `medium` | `opencli boss chatmsg "<uid>" [--page <page>] [--side "<auto\|boss\|geek>"] -f json`<br>BOSS直聘查看聊天消息历史（招聘端/求职端） | `uid` (str, required, positional); `page` (int, optional, default=1); `side` (str, optional, default='auto', choices=auto,boss,geek) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `joblist` | `private_content_read` / `medium` | `opencli boss joblist -f json`<br>BOSS直聘查看我发布的职位列表 | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `recommend` | `private_content_read` / `medium` | `opencli boss recommend [--limit <limit>] -f json`<br>BOSS直聘查看推荐候选人（新招呼列表） | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `resume` | `private_content_read` / `medium` | `opencli boss resume "<uid>" -f json`<br>BOSS直聘查看候选人简历（招聘端） | `uid` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `stats` | `private_content_read` / `medium` | `opencli boss stats [--job-id "<job-id>"] -f json`<br>BOSS直聘职位数据统计 | `job-id` (str, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `chatlist`: sensitive output: private content, account identifiers
- `chatmsg`: sensitive output: private content, account identifiers
- `joblist`: sensitive output: private content, account identifiers
- `recommend`: sensitive output: private content, account identifiers
- `resume`: sensitive output: private content, account identifiers
- `stats`: sensitive output: private content, account identifiers
