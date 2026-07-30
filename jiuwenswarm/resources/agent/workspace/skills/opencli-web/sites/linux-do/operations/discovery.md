# Linux Do: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `categories` | `public_read` / `low` | `opencli linux-do categories [--subcategories <true\|false>] [--limit <limit>] -f json`<br>linux.do 分类列表 | `subcategories` (boolean, optional, default=False); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli linux-do search "<query>" [--limit <limit>] -f json`<br>搜索 linux.do | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `tags` | `public_read` / `low` | `opencli linux-do tags [--limit <limit>] -f json`<br>linux.do 标签列表 | `limit` (int, optional, default=30) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user-posts` | `public_read` / `low` | `opencli linux-do user-posts "<username>" [--limit <limit>] -f json`<br>linux.do 用户的帖子 | `username` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user-topics` | `public_read` / `low` | `opencli linux-do user-topics "<username>" [--limit <limit>] -f json`<br>linux.do 用户创建的话题 | `username` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `categories`: Source-audited against OpenCLI 1.8.6 linux-do/categories.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `search`: Source-audited against OpenCLI 1.8.6 linux-do/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `tags`: Source-audited against OpenCLI 1.8.6 linux-do/tags.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `user-posts`: Source-audited against OpenCLI 1.8.6 linux-do/user-posts.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `user-topics`: Source-audited against OpenCLI 1.8.6 linux-do/user-topics.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
