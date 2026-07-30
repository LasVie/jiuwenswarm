# Jimeng: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `history` | `private_content_read` / `medium` | `opencli jimeng history [--limit <limit>] -f json`<br>即梦AI 查看最近生成的作品 | `limit` (int, optional, default=5) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `workspaces` | `private_content_read` / `medium` | `opencli jimeng workspaces -f json`<br>即梦AI 查看所有工作区（会话窗口） | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `history`: Source-audited against OpenCLI 1.8.6 jimeng/history.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private generated-work metadata, account identifiers
- `workspaces`: Source-audited against OpenCLI 1.8.6 jimeng/workspaces.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private generated-work metadata, account identifiers
