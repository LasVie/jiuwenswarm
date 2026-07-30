# Xiaoyuzhou: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli xiaoyuzhou download "<id>" [--output "<output>"] -f json`<br>Download Xiaoyuzhou episode audio | `id` (str, required, positional); `output` (str, optional, default='./xiaoyuzhou-downloads') | auth=required; transport=local; fallback_before=browser_agent; fallback_after=none |
| `transcript` | `local_write` / `high` | `opencli xiaoyuzhou transcript "<id>" [--output "<output>"] [--json <true\|false>] [--text <true\|false>] -f json`<br>Download Xiaoyuzhou transcript as JSON and text (requires local credentials) | `id` (str, required, positional); `output` (str, optional, default='./xiaoyuzhou-transcripts'); `json` (boolean, optional, default=True); `text` (boolean, optional, default=True) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
- `transcript`: file outputs: workspace-relative output
