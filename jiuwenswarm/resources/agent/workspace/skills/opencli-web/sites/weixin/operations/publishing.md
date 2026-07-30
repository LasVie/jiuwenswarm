# Weixin: publishing

Publish, create, edit, or upload remote content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `create-draft` | `public_write` / `high` | `opencli weixin create-draft --title "<title>" "<content>" [--author "<author>"] [--cover-image "<cover-image>"] [--summary "<summary>"] [--timeout <timeout>] -f json`<br>创建微信公众号图文草稿 | `title` (str, required); `content` (str, required, positional); `author` (str, optional); `cover-image` (str, optional); `summary` (str, optional); `timeout` (int, optional, default=180) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `create-draft`: file inputs: workspace-relative input when declared by adapter
