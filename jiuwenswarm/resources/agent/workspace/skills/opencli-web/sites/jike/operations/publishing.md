# Jike: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `create` | `public_write` / `high` | `opencli jike create "<text>" -f json`<br>发布即刻动态 | `text` (string, required, positional) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `create`: file inputs: workspace-relative input when declared by adapter
