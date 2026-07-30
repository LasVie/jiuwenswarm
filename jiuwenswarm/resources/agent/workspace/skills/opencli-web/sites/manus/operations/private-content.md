# Manus: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `list` | `private_content_read` / `medium` | `opencli manus list [--limit <limit>] [--archived <true\|false>] -f json`<br>List Manus sessions (tasks). | `limit` (int, optional, default=20); `archived` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `read` | `private_content_read` / `medium` | `opencli manus read "<uid>" -f json`<br>Show details for a specific Manus session. | `uid` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `list`: Source-audited against OpenCLI 1.8.6 manus/list.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private task content, account identifiers
- `read`: Source-audited against OpenCLI 1.8.6 manus/read.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private task content, account identifiers
