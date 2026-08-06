# Midjourney: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli midjourney download "<job>" [--index "<index>"] [--kind "<kind>"] [--output "<output>"] [--force <true\|false>] -f json`<br>Download original images, raw video, social MP4, or GIF with MIME and atomic-write checks | `job` (str, required, positional); `index` (str, optional, default='all'); `kind` (str, optional, default='auto'); `output` (str, optional, default='~/Pictures/Midjourney'); `force` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
