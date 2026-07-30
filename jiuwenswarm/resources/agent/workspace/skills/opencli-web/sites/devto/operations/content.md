# Devto: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `latest` | `public_read` / `low` | `opencli devto latest [--limit <limit>] [--page <page>] -f json`<br>Newest dev.to articles (firehose, all tags) | `limit` (int, optional, default=20); `page` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `read` | `public_read` / `low` | `opencli devto read "<id>" [--max-length <max-length>] -f json`<br>Read a DEV.to article body by id | `id` (str, required, positional); `max-length` (int, optional, default=20000) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `tag` | `public_read` / `low` | `opencli devto tag "<tag>" [--limit <limit>] -f json`<br>Latest DEV.to articles for a specific tag | `tag` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top` | `public_read` / `low` | `opencli devto top [--limit <limit>] -f json`<br>Top DEV.to articles of the day | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli devto user "<username>" [--limit <limit>] -f json`<br>Recent DEV.to articles from a specific user | `username` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
