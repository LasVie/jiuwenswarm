# Slock: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `attachment-download` | `local_write` / `high` | `opencli slock attachment-download "<attachmentId>" [--out "<out>"] [--server "<server>"] -f json`<br>Download an attachment to a local file. Resolves a signed CDN URL in the page, then fetches bytes node-side (no CORS). | `attachmentId` (str, required, positional); `out` (str, optional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `channel-archive` | `local_write` / `high` | `opencli slock channel-archive "<channel>" [--server "<server>"] -f json`<br>Archive a channel — admin only (POST /channels/:id/archive) | `channel` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `attachment-download`: file outputs: workspace-relative output
- `channel-archive`: file outputs: workspace-relative output
