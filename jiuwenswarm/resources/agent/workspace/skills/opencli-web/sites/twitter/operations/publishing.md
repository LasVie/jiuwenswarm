# Twitter: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `list-create` | `public_write` / `high` | `opencli twitter list-create "<name>" [--description "<description>"] [--mode "<mode>"] -f json`<br>Create a new Twitter/X list (returns the new list id) | `name` (string, required, positional); `description` (string, optional, default=''); `mode` (string, optional, default='public') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `post` | `public_write` / `high` | `opencli twitter post "<text>" [--images "<images>"] -f json`<br>Post a new tweet/thread | `text` (string, required, positional); `images` (string, optional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `list-create`: file inputs: workspace-relative input when declared by adapter
- `post`: file inputs: workspace-relative input when declared by adapter
