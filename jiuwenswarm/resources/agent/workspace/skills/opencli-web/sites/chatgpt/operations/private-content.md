# Chatgpt: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `deep-research-result` | `private_content_read` / `medium` | `opencli chatgpt deep-research-result "<id>" [--wait <true\|false>] [--timeout <timeout>] [--stable <stable>] -f json`<br>Read a completed ChatGPT Deep Research report from the conversation payload | `id` (str, required, positional); `wait` (boolean, optional, default=False); `timeout` (int, optional, default=120); `stable` (int, optional, default=6) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `detail` | `private_content_read` / `medium` | `opencli chatgpt detail "<id>" [--markdown <true\|false>] [--wait <true\|false>] [--timeout <timeout>] [--stable <stable>] -f json`<br>Open a ChatGPT web conversation by ID and read its messages | `id` (str, required, positional); `markdown` (boolean, optional, default=False); `wait` (boolean, optional, default=False); `timeout` (int, optional, default=120); `stable` (int, optional, default=6) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli chatgpt history [--limit <limit>] -f json`<br>List visible ChatGPT web conversation history from the sidebar | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `project-list` | `private_content_read` / `medium` | `opencli chatgpt project-list [--limit <limit>] -f json`<br>List visible ChatGPT projects from the sidebar | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `read` | `private_content_read` / `medium` | `opencli chatgpt read [--markdown <true\|false>] -f json`<br>Read messages in the current ChatGPT web conversation | `markdown` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `deep-research-result`: Source-audited against OpenCLI 1.8.6 chatgpt/deep-research-result.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `detail`: Source-audited against OpenCLI 1.8.6 chatgpt/detail.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `history`: Source-audited against OpenCLI 1.8.6 chatgpt/history.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
- `project-list`: Source-audited against OpenCLI 1.8.6 chatgpt/project-list.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private project metadata, account identifiers
- `read`: Source-audited against OpenCLI 1.8.6 chatgpt/read.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private conversation content, account identifiers
