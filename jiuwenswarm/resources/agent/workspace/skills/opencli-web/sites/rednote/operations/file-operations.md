# Rednote: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli rednote download "<note-id>" [--output "<output>"] -f json`<br>Download images and videos from a rednote note | `note-id` (str, required, positional); `output` (str, optional, default='./rednote-downloads') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
