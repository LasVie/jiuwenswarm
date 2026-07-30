# Pixiv: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli pixiv download "<illust-id>" [--output "<output>"] -f json`<br>Download illustration images from Pixiv | `illust-id` (str, required, positional); `output` (str, optional, default='./pixiv-downloads') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
