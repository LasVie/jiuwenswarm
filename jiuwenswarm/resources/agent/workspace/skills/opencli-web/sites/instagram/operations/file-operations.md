# Instagram: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli instagram download "<url>" [--path "<path>"] -f json`<br>Download images and videos from Instagram posts and reels | `url` (str, required, positional); `path` (str, optional, default='~/Downloads/Instagram') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
