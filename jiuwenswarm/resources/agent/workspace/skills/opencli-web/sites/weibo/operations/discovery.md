# Weibo: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli weibo hot [--limit <limit>] -f json`<br>微博热搜 | `limit` (int, optional, default=30) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli weibo search "<keyword>" [--limit <limit>] -f json`<br>搜索微博 | `keyword` (str, required, positional); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user-posts` | `public_read` / `low` | `opencli weibo user-posts "<id>" [--start "<start>"] [--end "<end>"] [--limit <limit>] [--include-retweets <true\|false>] -f json`<br>List Weibo posts from a user, optionally filtered by date range | `id` (str, required, positional); `start` (str, optional); `end` (str, optional); `limit` (int, optional, default=20); `include-retweets` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `hot`: Source-audited against OpenCLI 1.8.6 weibo/hot.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `search`: Source-audited against OpenCLI 1.8.6 weibo/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user-posts`: Source-audited against OpenCLI 1.8.6 weibo/user-posts.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
