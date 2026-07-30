# 1Point3Acres: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `digest` | `public_read` / `low` | `opencli 1point3acres digest [--limit <limit>] -f json`<br>一亩三分地 精华帖（编辑推荐 / 加精） | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `forum` | `public_read` / `low` | `opencli 1point3acres forum "<fid>" [--page <page>] [--limit <limit>] -f json`<br>浏览一亩三分地某个版块的帖子列表（按 fid） | `fid` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `forums` | `public_read` / `low` | `opencli 1point3acres forums [--filter "<filter>"] -f json`<br>一亩三分地 所有版块（fid + 版块名） | `filter` (string, optional, default='') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `hot` | `public_read` / `low` | `opencli 1point3acres hot [--limit <limit>] -f json`<br>一亩三分地 今日热门帖子（按热度排序，约 50 条） | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `latest` | `public_read` / `low` | `opencli 1point3acres latest [--limit <limit>] -f json`<br>一亩三分地 最新发帖（按发帖时间倒序） | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `thread` | `public_read` / `low` | `opencli 1point3acres thread "<tid>" [--page <page>] [--limit <limit>] [--contentLimit <contentLimit>] -f json`<br>一亩三分地 帖子详情 + 楼层（主楼 + 回复） | `tid` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=10); `contentLimit` (int, optional, default=400) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli 1point3acres user "<who>" -f json`<br>一亩三分地 用户空间（用户组 / 积分 / 大米 / 帖子数 等） | `who` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
