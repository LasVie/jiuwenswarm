# Weibo: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `publish` | `public_write` / `high` | `opencli weibo publish "<text>" [--images "<images>"] -f json`<br>Publish a new Weibo post immediately | `text` (string, required, positional); `images` (string, optional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `publish`: file inputs: workspace-relative input when declared by adapter
