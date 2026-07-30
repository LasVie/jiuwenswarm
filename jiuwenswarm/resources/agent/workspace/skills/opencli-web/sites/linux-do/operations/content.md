# Linux Do: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `topic` | `public_read` / `low` | `opencli linux-do topic <id> [--limit <limit>] -f json`<br>linux.do 帖子首页摘要和回复（首屏） | `id` (int, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `topic-content` | `public_read` / `low` | `opencli linux-do topic-content <id> -f json`<br>Get the main topic body as Markdown | `id` (int, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `topic`: Source-audited against OpenCLI 1.8.6 linux-do/topic.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `topic-content`: Source-audited against OpenCLI 1.8.6 linux-do/topic-content.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
