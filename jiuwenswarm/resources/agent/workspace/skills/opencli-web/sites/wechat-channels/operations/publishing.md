# Wechat Channels: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `publish` | `public_write` / `high` | `opencli wechat-channels publish "<video>" [--title "<title>"] [--caption "<caption>"] [--schedule "<schedule>"] [--draft <true\|false>] [--manual <true\|false>] [--timeout <timeout>] -f json`<br>发布视频到视频号 | `video` (str, required, positional); `title` (str, optional); `caption` (str, optional); `schedule` (str, optional); `draft` (bool, optional, default=False); `manual` (bool, optional, default=False); `timeout` (int, optional, default=600) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `publish`: file inputs: workspace-relative input when declared by adapter
