# Bilibili: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `dynamic` | `private_content_read` / `medium` | `opencli bilibili dynamic [--limit <limit>] -f json`<br>Get Bilibili user dynamic feed | `limit` (int, optional, default=15) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `favorite` | `private_content_read` / `medium` | `opencli bilibili favorite [--fid <fid>] [--limit <limit>] [--page <page>] -f json`<br>我的收藏夹 | `fid` (int, optional); `limit` (int, optional, default=20); `page` (int, optional, default=1) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `feed` | `private_content_read` / `medium` | `opencli bilibili feed ["<uid>"] [--limit <limit>] [--type "<type>"] [--pages <pages>] -f json`<br>动态时间线（不传 uid 查关注时间线，传 uid 查指定用户动态） | `uid` (str, optional, positional); `limit` (int, optional, default=20); `type` (str, optional, default='all'); `pages` (int, optional, default=1) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `feed-detail` | `private_content_read` / `medium` | `opencli bilibili feed-detail "<id>" -f json`<br>查看 Bilibili 动态详情（支持充电专属内容） | `id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `following` | `private_content_read` / `medium` | `opencli bilibili following ["<uid>"] [--page <page>] [--limit <limit>] -f json`<br>获取 Bilibili 用户的关注列表 | `uid` (str, optional, positional); `page` (int, optional, default=1); `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli bilibili history [--limit <limit>] -f json`<br>我的观看历史 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `dynamic`: sensitive output: private content, account identifiers
- `favorite`: Source-audited against OpenCLI 1.8.6. Although upstream declares access=write, this command only reads favorite folders and resources.; sensitive output: private content, account identifiers
- `feed`: sensitive output: private content, account identifiers
- `feed-detail`: sensitive output: private content, account identifiers
- `following`: sensitive output: private content, account identifiers
- `history`: sensitive output: private content, account identifiers
