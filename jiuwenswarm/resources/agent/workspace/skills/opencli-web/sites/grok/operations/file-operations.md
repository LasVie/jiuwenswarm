# Grok: file-operations

Create or download workspace files.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `export-all` | `local_write` / `high` | `opencli grok export-all [--limit <limit>] [--offset <offset>] [--manifestPath "<manifestPath>"] [--maxScrolls <maxScrolls>] [--pageScrolls <pageScrolls>] [--pageTimeoutMs <pageTimeoutMs>] [--delayMinMs <delayMinMs>] [--delayMaxMs <delayMaxMs>] -f json`<br>Export Grok conversation history and each conversation transcript | `limit` (int, optional, default=0); `offset` (int, optional, default=0); `manifestPath` (string, optional, default=''); `maxScrolls` (int, optional, default=80); `pageScrolls` (int, optional, default=30); `pageTimeoutMs` (int, optional, default=30000); `delayMinMs` (int, optional, default=0); `delayMaxMs` (int, optional, default=5000) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `export-all`: file outputs: workspace-relative output
