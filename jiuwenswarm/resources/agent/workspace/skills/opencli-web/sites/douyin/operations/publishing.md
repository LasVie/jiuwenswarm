# Douyin: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `publish` | `public_write` / `high` | `opencli douyin publish "<video>" --title "<title>" --schedule "<schedule>" [--caption "<caption>"] [--cover "<cover>"] [--visibility "<public\|friends\|private>"] [--allow_download <true\|false>] [--collection "<collection>"] [--activity "<activity>"] [--poi_id "<poi_id>"] [--poi_name "<poi_name>"] [--hotspot "<hotspot>"] [--no_safety_check <true\|false>] [--sync_toutiao <true\|false>] -f json`<br>定时发布视频到抖音（必须设置 2h ~ 14天后的发布时间） | `video` (str, required, positional); `title` (str, required); `schedule` (str, required); `caption` (str, optional, default=''); `cover` (str, optional, default=''); `visibility` (str, optional, default='public', choices=public,friends,private); `allow_download` (bool, optional, default=False); `collection` (str, optional, default=''); `activity` (str, optional, default=''); `poi_id` (str, optional, default=''); `poi_name` (str, optional, default=''); `hotspot` (str, optional, default=''); `no_safety_check` (bool, optional, default=False); `sync_toutiao` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `update` | `public_write` / `high` | `opencli douyin update "<aweme_id>" [--reschedule "<reschedule>"] [--caption "<caption>"] -f json`<br>更新视频信息 | `aweme_id` (str, required, positional); `reschedule` (str, optional, default=''); `caption` (str, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `publish`: file inputs: workspace-relative input when declared by adapter
- `update`: file inputs: workspace-relative input when declared by adapter
