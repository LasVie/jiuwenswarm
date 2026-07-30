# Instagram: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `followers` | `private_content_read` / `medium` | `opencli instagram followers "<username>" [--limit <limit>] -f json`<br>List followers of an Instagram user | `username` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `following` | `private_content_read` / `medium` | `opencli instagram following "<username>" [--limit <limit>] -f json`<br>List accounts an Instagram user is following | `username` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `saved` | `private_content_read` / `medium` | `opencli instagram saved [--limit <limit>] [--collection "<collection>"] -f json`<br>Get your saved Instagram posts (optionally from a specific collection) | `limit` (int, optional, default=20); `collection` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user` | `private_content_read` / `medium` | `opencli instagram user "<username>" [--limit <limit>] -f json`<br>Get recent posts from an Instagram user | `username` (str, required, positional); `limit` (int, optional, default=12) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `followers`: Source-audited against OpenCLI 1.8.6 instagram/followers.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: social graph, account identifiers
- `following`: Source-audited against OpenCLI 1.8.6 instagram/following.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: social graph, account identifiers
- `saved`: Source-audited against OpenCLI 1.8.6 instagram/saved.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: saved content, account identifiers
- `user`: Source-audited against OpenCLI 1.8.6 instagram/user.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private social content, account identifiers
