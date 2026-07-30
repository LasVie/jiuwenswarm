# Grok: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `private_content_read` / `medium` | `opencli grok detail "<id>" [--markdown <true\|false>] -f json`<br>Open a Grok conversation by ID and read its messages | `id` (str, required, positional); `markdown` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `export` | `private_content_read` / `medium` | `opencli grok export [--limit <limit>] [--maxScrolls <maxScrolls>] -f json`<br>Export all visible Grok conversation history metadata | `limit` (int, optional, default=0); `maxScrolls` (int, optional, default=80) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli grok history [--limit <limit>] -f json`<br>List recent Grok conversations from the sidebar (requires login) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `read` | `private_content_read` / `medium` | `opencli grok read [--markdown <true\|false>] -f json`<br>Read messages in the current Grok conversation | `markdown` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 grok/detail.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `export`: Source-audited against OpenCLI 1.8.6 grok/export.js; returns private conversation metadata as command output and does not create a local export file.; file outputs: workspace-relative output; sensitive output: private conversation metadata, account identifiers
- `history`: Source-audited against OpenCLI 1.8.6 grok/history.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `read`: Source-audited against OpenCLI 1.8.6 grok/read.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
