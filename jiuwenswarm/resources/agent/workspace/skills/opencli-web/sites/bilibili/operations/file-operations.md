# Bilibili: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli bilibili download "<bvid>" [--output "<output>"] [--quality "<quality>"] [--force <true\|false>] [--page "<page>"] -f json`<br>下载B站视频（需要 yt-dlp） | `bvid` (str, required, positional); `output` (str, optional, default='./bilibili-downloads'); `quality` (str, optional, default='best'); `force` (boolean, optional, default=False); `page` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
