# Doubao: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `meeting-transcript` | `local_write` / `high` | `opencli doubao meeting-transcript "<id>" [--download "<download>"] -f json`<br>Get or download the meeting transcript from a Doubao conversation | `id` (str, required, positional); `download` (str, optional, default='false') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `meeting-transcript`: file outputs: workspace-relative output
