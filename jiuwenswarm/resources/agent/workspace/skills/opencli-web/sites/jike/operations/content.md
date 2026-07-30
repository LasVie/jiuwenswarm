# Jike: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `post` | `public_read` / `low` | `opencli jike post "<id>" -f json`<br>即刻帖子详情及评论 | `id` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `topic` | `public_read` / `low` | `opencli jike topic "<id>" [--limit <limit>] -f json`<br>即刻话题/圈子帖子 | `id` (string, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli jike user "<username>" [--limit <limit>] -f json`<br>即刻用户动态 | `username` (string, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `post`: Source-audited against OpenCLI 1.8.6 jike/post.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `topic`: Source-audited against OpenCLI 1.8.6 jike/topic.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `user`: Source-audited against OpenCLI 1.8.6 jike/user.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
