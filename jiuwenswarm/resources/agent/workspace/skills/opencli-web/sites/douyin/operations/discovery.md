# Douyin: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `location` | `public_read` / `low` | `opencli douyin location "<query>" [--limit <limit>] -f json`<br>地理位置 POI 搜索 | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `public_read` / `low` | `opencli douyin search "<query>" [--limit <limit>] -f json`<br>关键词搜索抖音视频 | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user-videos` | `public_read` / `low` | `opencli douyin user-videos "<sec_uid>" [--limit <limit>] [--with_comments <true\|false>] [--comment_limit <comment_limit>] -f json`<br>获取指定用户的视频列表（含下载地址和热门评论） | `sec_uid` (string, required, positional); `limit` (int, optional, default=20); `with_comments` (bool, optional, default=True); `comment_limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
