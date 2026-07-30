# Twitter: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `article` | `public_read` / `low` | `opencli twitter article "<tweet-id>" -f json`<br>Fetch a Twitter Article (long-form content) and export as Markdown | `tweet-id` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `profile` | `public_read` / `low` | `opencli twitter profile ["<username>"] -f json`<br>Fetch a Twitter user profile — bio, stats, etc. (defaults to the logged-in user when no username is given) | `username` (string, optional, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `thread` | `public_read` / `low` | `opencli twitter thread "<tweet-id>" [--limit <limit>] [--top-by-engagement <top-by-engagement>] -f json`<br>Get a tweet thread (original + all replies) | `tweet-id` (string, required, positional); `limit` (int, optional, default=50); `top-by-engagement` (int, optional, default=0) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `tweets` | `public_read` / `low` | `opencli twitter tweets ["<username>"] [--limit <limit>] [--page-delay <page-delay>] [--top-by-engagement <top-by-engagement>] -f json`<br>Fetch a Twitter user's most recent tweets (chronological, excludes pinned; defaults to the logged-in user when no username is given) | `username` (string, optional, positional); `limit` (int, optional, default=20); `page-delay` (int, optional, default=2); `top-by-engagement` (int, optional, default=0) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `article`: Source-audited against OpenCLI 1.8.6 twitter/article.js; returns public long-form content as Markdown command output without creating a local file.
- `profile`: Source-audited against OpenCLI 1.8.6 twitter/profile.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `thread`: Source-audited against OpenCLI 1.8.6 twitter/thread.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `tweets`: Source-audited against OpenCLI 1.8.6 twitter/tweets.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
