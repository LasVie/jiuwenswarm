# Youtube: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `private_content_read` / `medium` | `opencli youtube feed [--limit <limit>] -f json`<br>Get YouTube homepage recommended videos | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli youtube history [--limit <limit>] -f json`<br>Get YouTube watch history | `limit` (int, optional, default=30) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `playlist` | `private_content_read` / `medium` | `opencli youtube playlist "<id>" [--limit <limit>] -f json`<br>Get YouTube playlist info and video list | `id` (str, required, positional); `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `subscriptions` | `private_content_read` / `medium` | `opencli youtube subscriptions [--limit <limit>] -f json`<br>List subscribed YouTube channels | `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `watch-later` | `private_content_read` / `medium` | `opencli youtube watch-later [--limit <limit>] -f json`<br>Get your YouTube Watch Later queue | `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `feed`: Source-audited against OpenCLI 1.8.6 youtube/feed.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private viewing data, account identifiers
- `history`: Source-audited against OpenCLI 1.8.6 youtube/history.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private viewing data, account identifiers
- `playlist`: Source-audited against OpenCLI 1.8.6 youtube/playlist.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private viewing data, account identifiers
- `subscriptions`: Source-audited against OpenCLI 1.8.6 youtube/subscriptions.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private viewing data, account identifiers
- `watch-later`: Source-audited against OpenCLI 1.8.6 youtube/watch-later.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private viewing data, account identifiers
