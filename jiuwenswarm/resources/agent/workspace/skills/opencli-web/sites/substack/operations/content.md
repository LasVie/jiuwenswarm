# Substack: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `publication` | `public_read` / `low` | `opencli substack publication "<url>" [--limit <limit>] -f json`<br>获取特定 Substack Newsletter 的最新文章 | `url` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
