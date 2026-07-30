# Instagram: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `collection-create` | `public_write` / `high` | `opencli instagram collection-create "<name>" -f json`<br>Create a new Instagram saved-posts collection (folder) | `name` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `post` | `public_write` / `high` | `opencli instagram post [--media "<media>"] ["<content>"] [--timeout <timeout>] -f json`<br>Post an Instagram feed image or mixed-media carousel | `media` (str, optional); `content` (str, optional, positional); `timeout` (int, optional, default=300) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `collection-create`: file inputs: workspace-relative input when declared by adapter
- `post`: file inputs: workspace-relative input when declared by adapter
