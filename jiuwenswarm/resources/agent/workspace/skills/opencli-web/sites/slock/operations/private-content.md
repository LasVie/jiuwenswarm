# Slock: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `attachment-url` | `private_content_read` / `medium` | `opencli slock attachment-url "<attachmentId>" [--server "<server>"] -f json`<br>Get a short-lived signed CDN URL for an attachment (does not download bytes). | `attachmentId` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `bookmark-list` | `private_content_read` / `medium` | `opencli slock bookmark-list [--limit <limit>] [--offset <offset>] [--server "<server>"] -f json`<br>List bookmarks (saved messages) in the active server | `limit` (int, optional, default=50); `offset` (int, optional, default=0); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `channel-files` | `private_content_read` / `medium` | `opencli slock channel-files "<channel>" [--limit <limit>] [--server "<server>"] -f json`<br>List files shared in a channel (GET /channels/:id/files) | `channel` (str, required, positional); `limit` (int, optional, default=50); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `channel-info` | `private_content_read` / `medium` | `opencli slock channel-info "<channel>" [--server "<server>"] -f json`<br>Show one channel's details (GET /channels/:id) | `channel` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `channel-list` | `private_content_read` / `medium` | `opencli slock channel-list [--server "<server>"] -f json`<br>List channels in the active slock server | `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `channel-members` | `private_content_read` / `medium` | `opencli slock channel-members "<channel>" [--server "<server>"] -f json`<br>List members of a channel | `channel` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `dm-list` | `private_content_read` / `medium` | `opencli slock dm-list [--server "<server>"] -f json`<br>List DM channels in the active server (GET /channels/dm) | `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `inbox` | `private_content_read` / `medium` | `opencli slock inbox [--filter "<filter>"] [--limit <limit>] [--offset <offset>] [--server "<server>"] -f json`<br>List unified inbox items (channels, DMs, followed threads) that need attention. | `filter` (str, optional, default='all'); `limit` (int, optional, default=30); `offset` (int, optional, default=0); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `message-read` | `private_content_read` / `medium` | `opencli slock message-read "<channel>" [--after "<after>"] [--before "<before>"] [--limit <limit>] [--no-threads <true\|false>] [--server "<server>"] -f json`<br>Read messages in a channel or thread. Thread form: "#channel:msgIdOrShort". Use --after seq\|UUID for cursor. | `channel` (str, required, positional); `after` (str, optional); `before` (str, optional); `limit` (int, optional, default=50); `no-threads` (bool, optional, default=False); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `message-search` | `private_content_read` / `medium` | `opencli slock message-search "<query>" [--channel "<channel>"] [--limit <limit>] [--server "<server>"] -f json`<br>Search messages | `query` (str, required, positional); `channel` (str, optional); `limit` (int, optional, default=50); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `server-list` | `private_content_read` / `medium` | `opencli slock server-list -f json`<br>List slock servers you belong to; marks active per localStorage slug | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `task-get` | `private_content_read` / `medium` | `opencli slock task-get "<channel>" "<number>" [--server "<server>"] -f json`<br>Fetch a task by channel + taskNumber (GET /tasks/channel/:channelId/number/:taskNumber). | `channel` (str, required, positional); `number` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `task-list` | `private_content_read` / `medium` | `opencli slock task-list "<channel>" [--status "<status>"] [--server "<server>"] -f json`<br>List tasks (chat tasks = messages with task fields) attached to a channel. Optional --status filter. | `channel` (str, required, positional); `status` (str, optional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `task-list-server` | `private_content_read` / `medium` | `opencli slock task-list-server [--status "<status>"] [--server "<server>"] -f json`<br>List tasks across all channels in the active server (GET /tasks/server). Optional --status filter. | `status` (str, optional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `thread-list` | `private_content_read` / `medium` | `opencli slock thread-list [--server "<server>"] -f json`<br>List followed threads in the active server (GET /channels/threads/followed) | `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `unread-summary` | `private_content_read` / `medium` | `opencli slock unread-summary -f json`<br>Global unread counts across every server you belong to. | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `attachment-url`: sensitive output: private content, account identifiers
- `bookmark-list`: sensitive output: private content, account identifiers
- `channel-files`: sensitive output: private content, account identifiers
- `channel-info`: sensitive output: private content, account identifiers
- `channel-list`: sensitive output: private content, account identifiers
- `channel-members`: sensitive output: private content, account identifiers
- `dm-list`: sensitive output: private content, account identifiers
- `inbox`: sensitive output: private content, account identifiers
- `message-read`: sensitive output: private content, account identifiers
- `message-search`: sensitive output: private content, account identifiers
- `server-list`: sensitive output: private content, account identifiers
- `task-get`: sensitive output: private content, account identifiers
- `task-list`: sensitive output: private content, account identifiers
- `task-list-server`: sensitive output: private content, account identifiers
- `thread-list`: sensitive output: private content, account identifiers
- `unread-summary`: sensitive output: private content, account identifiers
