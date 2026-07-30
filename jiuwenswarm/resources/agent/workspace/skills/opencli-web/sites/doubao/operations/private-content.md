# Doubao: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `private_content_read` / `medium` | `opencli doubao detail "<id>" -f json`<br>Read a specific Doubao conversation by ID | `id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli doubao history [--limit "<limit>"] -f json`<br>List conversation history from Doubao sidebar | `limit` (str, optional, default='50') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `meeting-summary` | `private_content_read` / `medium` | `opencli doubao meeting-summary "<id>" [--chapters "<chapters>"] -f json`<br>Get meeting summary and chapters from a Doubao conversation | `id` (str, required, positional); `chapters` (str, optional, default='false') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `read` | `private_content_read` / `medium` | `opencli doubao read -f json`<br>Read the current Doubao conversation history | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 doubao/detail.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `history`: Source-audited against OpenCLI 1.8.6 doubao/history.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `meeting-summary`: Source-audited against OpenCLI 1.8.6 doubao/meeting-summary.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private meeting content, account identifiers
- `read`: Source-audited against OpenCLI 1.8.6 doubao/read.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
