# Bilibili: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comments` | `public_read` / `low` | `opencli bilibili comments "<bvid>" [--parent <parent>] [--limit <limit>] -f json`<br>获取 B站视频评论（官方 API；用 --parent <rpid> 读取某条评论下的「楼中楼」回复） | `bvid` (str, required, positional); `parent` (int, optional); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `subtitle` | `public_read` / `low` | `opencli bilibili subtitle "<bvid>" [--lang "<lang>"] [--page "<page>"] -f json`<br>获取 Bilibili 视频的字幕 | `bvid` (str, required, positional); `lang` (str, optional); `page` (str, optional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `summary` | `public_read` / `low` | `opencli bilibili summary "<bvid>" -f json`<br>获取 B站视频的官方 AI 总结（视频页「AI总结」同款，含分段大纲与时间戳） | `bvid` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user-videos` | `public_read` / `low` | `opencli bilibili user-videos "<uid>" [--limit <limit>] [--order "<order>"] [--page <page>] -f json`<br>查看指定用户的投稿视频 | `uid` (str, required, positional); `limit` (int, optional, default=20); `order` (str, optional, default='pubdate'); `page` (int, optional, default=1) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `video` | `public_read` / `low` | `opencli bilibili video "<bvid>" [--page "<page>"] -f json`<br>Get Bilibili video metadata (title, author, duration, stats, etc.) | `bvid` (str, required, positional); `page` (str, optional) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
