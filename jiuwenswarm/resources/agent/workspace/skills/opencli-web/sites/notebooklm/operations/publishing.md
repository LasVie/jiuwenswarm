# Notebooklm: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `create` | `public_write` / `high` | `opencli notebooklm create "<title>" [--emoji "<emoji>"] [--execute <true\|false>] -f json`<br>Create a new NotebookLM notebook with the given title | `title` (str, required, positional); `emoji` (str, optional); `execute` (boolean, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `create`: file inputs: workspace-relative input when declared by adapter
