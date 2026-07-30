# Xiaohongshu: creator-analytics

Read creator account and note performance metrics.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `creator-note-detail` | `private_content_read` / `medium` | `opencli xiaohongshu creator-note-detail "<note-id>" -f json`<br>小红书单篇笔记详情页数据 (笔记信息 + 核心/互动数据 + 观看来源 + 观众画像 + 趋势数据) | `note-id` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `creator-notes` | `private_content_read` / `medium` | `opencli xiaohongshu creator-notes [--limit <limit>] -f json`<br>小红书创作者笔记列表 + 每篇数据 (标题/日期/观看/点赞/收藏/评论) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `creator-notes-summary` | `private_content_read` / `medium` | `opencli xiaohongshu creator-notes-summary [--limit <limit>] [--timeout <timeout>] -f json`<br>小红书最近笔记批量摘要 (列表 + 单篇关键数据汇总) | `limit` (int, optional, default=3); `timeout` (int, optional, default=180) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `creator-profile` | `private_account_read` / `medium` | `opencli xiaohongshu creator-profile -f json`<br>小红书创作者账号信息 (粉丝/关注/获赞/成长等级) | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `creator-stats` | `private_content_read` / `medium` | `opencli xiaohongshu creator-stats [--period "<seven\|thirty>"] -f json`<br>小红书创作者数据总览 (观看/点赞/收藏/评论/分享/涨粉，含每日趋势) | `period` (string, optional, default='seven', choices=seven,thirty) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `creator-note-detail`: sensitive output: private content, account identifiers
- `creator-notes`: sensitive output: private content, account identifiers
- `creator-notes-summary`: sensitive output: private content, account identifiers
- `creator-profile`: sensitive output: account identifiers
- `creator-stats`: sensitive output: private content, account identifiers
