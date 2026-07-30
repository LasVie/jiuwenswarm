# Sinablog: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `article` | `public_read` / `low` | `opencli sinablog article "<url>" -f json`<br>获取新浪博客单篇文章详情 | `url` (str, required, positional) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user` | `public_read` / `low` | `opencli sinablog user "<uid>" [--limit <limit>] -f json`<br>获取新浪博客用户的文章列表 | `uid` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
