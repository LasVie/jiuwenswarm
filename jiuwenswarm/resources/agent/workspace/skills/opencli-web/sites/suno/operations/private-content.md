# Suno: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `list` | `private_content_read` / `medium` | `opencli suno list [--limit <limit>] [--page <page>] -f json`<br>List recent Suno clips in your library (id, title, status, created_at, link) | `limit` (int, optional, default=20); `page` (int, optional, default=0) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `list`: sensitive output: private content, account identifiers
