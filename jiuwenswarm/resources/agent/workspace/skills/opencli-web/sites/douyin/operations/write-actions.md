# Douyin: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `draft` | `reversible_remote_write` / `high` | `opencli douyin draft "<video>" --title "<title>" [--caption "<caption>"] [--cover "<cover>"] [--visibility "<public\|friends\|private>"] -f json`<br>上传视频并保存为草稿 | `video` (str, required, positional); `title` (str, required); `caption` (str, optional, default=''); `cover` (str, optional, default=''); `visibility` (str, optional, default='public', choices=public,friends,private) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
