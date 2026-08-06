# Douyin: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `activities` | `private_content_read` / `medium` | `opencli douyin activities -f json`<br>官方活动列表 | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `collections` | `private_content_read` / `medium` | `opencli douyin collections [--limit <limit>] -f json`<br>合集列表 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `drafts` | `private_content_read` / `medium` | `opencli douyin drafts [--limit <limit>] -f json`<br>获取草稿列表 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `hashtag` | `private_content_read` / `medium` | `opencli douyin hashtag "<search\|suggest\|hot>" [--keyword "<keyword>"] [--cover "<cover>"] [--limit <limit>] -f json`<br>话题搜索 / AI推荐 / 热点词 | `action` (str, required, positional, choices=search,suggest,hot); `keyword` (str, optional, default=''); `cover` (str, optional, default=''); `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `stats` | `private_content_read` / `medium` | `opencli douyin stats "<aweme_id>" -f json`<br>作品数据分析 | `aweme_id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `videos` | `private_content_read` / `medium` | `opencli douyin videos [--limit <limit>] [--status "<all\|published\|reviewing\|scheduled>"] -f json`<br>获取作品列表 | `limit` (int, optional, default=20); `status` (str, optional, default='all', choices=all,published,reviewing,scheduled) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `activities`: sensitive output: private content, account identifiers
- `collections`: sensitive output: private content, account identifiers
- `drafts`: sensitive output: private content, account identifiers
- `hashtag`: sensitive output: private content, account identifiers
- `stats`: sensitive output: private content, account identifiers
- `videos`: sensitive output: private content, account identifiers
