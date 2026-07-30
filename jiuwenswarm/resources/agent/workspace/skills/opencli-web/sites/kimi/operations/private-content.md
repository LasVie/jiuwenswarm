# Kimi: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `private_content_read` / `medium` | `opencli kimi detail "<id>" [--limit <limit>] -f json`<br>Open a Kimi chat by ID and return its visible messages. | `id` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `history` | `private_content_read` / `medium` | `opencli kimi history [--limit <limit>] -f json`<br>List recent Kimi chats from the sidebar (with chat IDs extracted from href). | `limit` (int, optional, default=30) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `read` | `private_content_read` / `medium` | `opencli kimi read [--conv "<conv>"] [--limit <limit>] -f json`<br>Read messages in the current Kimi chat. Pass --conv <id> to navigate to a specific chat first. | `conv` (str, optional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 kimi/chat.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private content, account identifiers
- `history`: Source-audited against OpenCLI 1.8.6 kimi/chat.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private content, account identifiers
- `read`: Source-audited against OpenCLI 1.8.6 kimi/chat.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private content, account identifiers
