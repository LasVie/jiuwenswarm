# Reddit: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `home` | `private_content_read` / `medium` | `opencli reddit home [--limit <limit>] -f json`<br>Reddit personalized home feed (Best, requires login) | `limit` (int, optional, default=25) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `saved` | `private_content_read` / `medium` | `opencli reddit saved [--limit <limit>] -f json`<br>Browse your saved Reddit posts | `limit` (int, optional, default=15) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `subscribed` | `private_content_read` / `medium` | `opencli reddit subscribed [--limit <limit>] -f json`<br>List subreddits you are subscribed to | `limit` (int, optional, default=100) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `upvoted` | `private_content_read` / `medium` | `opencli reddit upvoted [--limit <limit>] -f json`<br>Browse your upvoted Reddit posts | `limit` (int, optional, default=15) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `home`: Source-audited against OpenCLI 1.8.6 reddit/home.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: personalized feed, account identifiers
- `saved`: Source-audited against OpenCLI 1.8.6 reddit/saved.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: account activity, account identifiers
- `subscribed`: Source-audited against OpenCLI 1.8.6 reddit/subscribed.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: account activity, account identifiers
- `upvoted`: Source-audited against OpenCLI 1.8.6 reddit/upvoted.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: account activity, account identifiers
