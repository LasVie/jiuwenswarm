# Tiktok: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `creator-videos` | `private_content_read` / `medium` | `opencli tiktok creator-videos [--limit <limit>] [--cursor "<cursor>"] -f json`<br>TikTok Studio creator content list (views/likes/comments/saves/shares) | `limit` (int, optional, default=20); `cursor` (string, optional, default='0') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `following` | `private_content_read` / `medium` | `opencli tiktok following [--limit <limit>] -f json`<br>List accounts the logged-in user follows on TikTok via page-context APIs | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `friends` | `private_content_read` / `medium` | `opencli tiktok friends [--limit <limit>] -f json`<br>Get TikTok friend / who-to-follow suggestions via page-context APIs | `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notifications` | `private_content_read` / `medium` | `opencli tiktok notifications [--limit <limit>] [--type "<all\|likes\|comments\|mentions\|followers>"] -f json`<br>Read TikTok inbox notifications (likes, comments, mentions, followers) via page-context APIs | `limit` (int, optional, default=15); `type` (str, optional, default='all', choices=all,likes,comments,mentions,followers) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `creator-videos`: Source-audited against OpenCLI 1.8.6 tiktok/creator-videos.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: creator analytics, account identifiers
- `following`: Source-audited against OpenCLI 1.8.6 tiktok/following.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: social graph, account identifiers
- `friends`: Source-audited against OpenCLI 1.8.6 tiktok/friends.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: personalized recommendations, account identifiers
- `notifications`: Source-audited against OpenCLI 1.8.6 tiktok/notifications.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private notifications, account identifiers
