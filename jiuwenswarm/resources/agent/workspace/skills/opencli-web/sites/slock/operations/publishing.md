# Slock: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `attachment-upload` | `public_write` / `high` | `opencli slock attachment-upload "<file>" "<channel>" [--server "<server>"] -f json`<br>Upload a local file to Slock attachments. Prints the attachmentId for use with `message-send --attach`. | `file` (str, required, positional); `channel` (str, required, positional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `channel-create` | `public_write` / `high` | `opencli slock channel-create "<name>" [--description "<description>"] [--private <true\|false>] [--server "<server>"] -f json`<br>Create a channel — admin only (POST /channels/). Public unless --private. | `name` (str, required, positional); `description` (str, optional); `private` (bool, optional, default=False); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `task-create` | `public_write` / `high` | `opencli slock task-create "<channel>" "<title>" [--desc "<desc>"] [--server "<server>"] -f json`<br>Create a task in a channel (single title; batch 1-50 is server-supported but client surface is single — see backlog R4). | `channel` (str, required, positional); `title` (str, required, positional); `desc` (str, optional); `server` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `attachment-upload`: file inputs: workspace-relative input when declared by adapter
- `channel-create`: file inputs: workspace-relative input when declared by adapter
- `task-create`: file inputs: workspace-relative input when declared by adapter
