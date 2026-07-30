# Suno: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli suno download "<clip>" [--formats "<formats>"] [--op "<op>"] [--confirm-paid <true\|false>] -f json`<br>Download an existing Suno clip (MP3 + optional WAV/M4A/video) by id | `clip` (str, required, positional); `formats` (str, optional); `op` (str, optional); `confirm-paid` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
