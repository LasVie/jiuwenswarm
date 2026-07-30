# Xueqiu: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comments` | `public_read` / `low` | `opencli xueqiu comments "<symbol>" [--limit <limit>] -f json`<br>获取单只股票的讨论动态 | `symbol` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `comments`: Source-audited against OpenCLI 1.8.6 xueqiu/comments.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
