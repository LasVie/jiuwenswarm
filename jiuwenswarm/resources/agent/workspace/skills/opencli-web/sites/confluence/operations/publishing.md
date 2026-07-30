# Confluence: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `create` | `public_write` / `high` | `opencli confluence create --space "<space>" --title "<title>" --file "<file>" [--parent "<parent>"] [--representation "<markdown\|storage>"] [--execute <true\|false>] -f json`<br>Create a Confluence page from Markdown or storage XHTML | `space` (string, required); `title` (string, required); `file` (string, required); `parent` (string, optional); `representation` (string, optional, default='markdown', choices=markdown,storage); `execute` (boolean, optional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `update` | `public_write` / `high` | `opencli confluence update "<id>" --file "<file>" [--title "<title>"] [--version-message "<version-message>"] [--representation "<markdown\|storage>"] [--execute <true\|false>] -f json`<br>Update a Confluence page body from Markdown or storage XHTML | `id` (str, required, positional); `file` (string, required); `title` (string, optional); `version-message` (string, optional); `representation` (string, optional, default='markdown', choices=markdown,storage); `execute` (boolean, optional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `create`: file inputs: workspace-relative input when declared by adapter
- `update`: file inputs: workspace-relative input when declared by adapter
