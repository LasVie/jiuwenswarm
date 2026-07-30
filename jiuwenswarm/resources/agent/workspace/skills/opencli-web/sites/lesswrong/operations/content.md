# Lesswrong: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comments` | `public_read` / `low` | `opencli lesswrong comments "<url-or-id>" [--limit <limit>] -f json`<br>Top comments on a post | `url-or-id` (string, required, positional); `limit` (int, optional, default=5) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `curated` | `public_read` / `low` | `opencli lesswrong curated [--limit <limit>] -f json`<br>Curated editor's picks | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `frontpage` | `public_read` / `low` | `opencli lesswrong frontpage [--limit <limit>] -f json`<br>Algorithmic frontpage | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `new` | `public_read` / `low` | `opencli lesswrong new [--limit <limit>] -f json`<br>Latest posts | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `read` | `public_read` / `low` | `opencli lesswrong read "<url-or-id>" -f json`<br>Read full post by URL or ID | `url-or-id` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `sequences` | `public_read` / `low` | `opencli lesswrong sequences [--limit <limit>] -f json`<br>List post collections | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `shortform` | `public_read` / `low` | `opencli lesswrong shortform [--limit <limit>] -f json`<br>Quick takes / shortform posts | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `tag` | `public_read` / `low` | `opencli lesswrong tag "<tag>" [--limit <limit>] -f json`<br>Posts by tag | `tag` (string, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `tags` | `public_read` / `low` | `opencli lesswrong tags [--limit <limit>] -f json`<br>List popular tags | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top` | `public_read` / `low` | `opencli lesswrong top [--limit <limit>] -f json`<br>Top all-time | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top-month` | `public_read` / `low` | `opencli lesswrong top-month [--limit <limit>] -f json`<br>Top this month | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top-week` | `public_read` / `low` | `opencli lesswrong top-week [--limit <limit>] -f json`<br>Top this week | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top-year` | `public_read` / `low` | `opencli lesswrong top-year [--limit <limit>] -f json`<br>Top this year | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli lesswrong user "<username>" -f json`<br>User profile | `username` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user-posts` | `public_read` / `low` | `opencli lesswrong user-posts "<username>" [--limit <limit>] -f json`<br>List a user's posts | `username` (string, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
