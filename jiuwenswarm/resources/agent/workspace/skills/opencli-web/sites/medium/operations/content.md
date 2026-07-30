# Medium: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `tag` | `public_read` / `low` | `opencli medium tag "<tag>" [--limit <limit>] -f json`<br>Latest Medium articles tagged with a given keyword (RSS feed) | `tag` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli medium user "<username>" [--limit <limit>] -f json`<br>获取 Medium 用户的文章列表 | `username` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
