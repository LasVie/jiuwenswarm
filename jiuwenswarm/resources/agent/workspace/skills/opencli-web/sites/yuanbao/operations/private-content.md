# Yuanbao: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `private_content_read` / `medium` | `opencli yuanbao detail "<id>" -f json`<br>Open a Yuanbao conversation by ID and read its messages | `id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli yuanbao history [--limit <limit>] -f json`<br>List recent Yuanbao conversations from the sidebar (requires login) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `read` | `private_content_read` / `medium` | `opencli yuanbao read -f json`<br>Read messages in the current Yuanbao conversation | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 yuanbao/detail.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `history`: Source-audited against OpenCLI 1.8.6 yuanbao/history.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `read`: Source-audited against OpenCLI 1.8.6 yuanbao/read.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
