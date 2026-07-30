# Quark: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `ls` | `private_content_read` / `medium` | `opencli quark ls ["<path>"] [--depth <depth>] [--dirs-only <true\|false>] -f json`<br>List files in your Quark Drive | `path` (str, optional, positional, default=''); `depth` (int, optional, default=0); `dirs-only` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `share-tree` | `private_content_read` / `medium` | `opencli quark share-tree "<url>" [--passcode "<passcode>"] [--depth <depth>] -f json`<br>Get directory tree from Quark Drive share link as nested JSON | `url` (str, required, positional); `passcode` (str, optional, default=''); `depth` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `ls`: sensitive output: private content, account identifiers
- `share-tree`: sensitive output: private content, account identifiers
