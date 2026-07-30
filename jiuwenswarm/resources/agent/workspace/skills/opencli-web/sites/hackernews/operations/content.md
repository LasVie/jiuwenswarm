# Hackernews: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ask` | `public_read` / `low` | `opencli hackernews ask [--limit <limit>] -f json`<br>Hacker News Ask HN posts | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `best` | `public_read` / `low` | `opencli hackernews best [--limit <limit>] -f json`<br>Hacker News best stories | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `jobs` | `public_read` / `low` | `opencli hackernews jobs [--limit <limit>] -f json`<br>Hacker News job postings | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `new` | `public_read` / `low` | `opencli hackernews new [--limit <limit>] -f json`<br>Hacker News newest stories | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `read` | `public_read` / `low` | `opencli hackernews read "<id>" [--limit <limit>] [--depth <depth>] [--replies <replies>] [--max-length <max-length>] -f json`<br>Read a Hacker News story and its comment tree | `id` (str, required, positional); `limit` (int, optional, default=25); `depth` (int, optional, default=2); `replies` (int, optional, default=5); `max-length` (int, optional, default=2000) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `show` | `public_read` / `low` | `opencli hackernews show [--limit <limit>] -f json`<br>Hacker News Show HN posts | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top` | `public_read` / `low` | `opencli hackernews top [--limit <limit>] -f json`<br>Hacker News top stories | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli hackernews user "<username>" -f json`<br>Hacker News user profile | `username` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `ask`: Public Ask HN feed read; this command does not create a post.
- `new`: Public newest-stories feed read; this command does not create content.
