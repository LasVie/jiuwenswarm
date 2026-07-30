# Producthunt: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `posts` | `public_read` / `low` | `opencli producthunt posts [--limit <limit>] [--category "<category>"] -f json`<br>Latest Product Hunt launches (optional category filter) | `limit` (int, optional, default=20); `category` (string, optional, default='') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `today` | `public_read` / `low` | `opencli producthunt today [--limit <limit>] -f json`<br>Today's Product Hunt launches (most recent day in feed) | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
