# Pinterest: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `download` | `local_write` / `high` | `opencli pinterest download "<pin>" [--output "<output>"] -f json`<br>Download a pin's original image to disk | `pin` (string, required, positional); `output` (string, optional, default='./pinterest-downloads') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `download`: file outputs: workspace-relative output
