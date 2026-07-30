# Qwen: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `private_content_read` / `medium` | `opencli qwen detail "<id>" [--markdown <true\|false>] -f json`<br>Open a Qianwen conversation by ID and read its messages | `id` (str, required, positional); `markdown` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli qwen history [--limit <limit>] -f json`<br>List recent Qianwen conversations (requires login) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `read` | `private_content_read` / `medium` | `opencli qwen read [--markdown <true\|false>] -f json`<br>Read messages in the current Qianwen conversation | `markdown` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 qwen/detail.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `history`: Source-audited against OpenCLI 1.8.6 qwen/history.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `read`: Source-audited against OpenCLI 1.8.6 qwen/read.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
