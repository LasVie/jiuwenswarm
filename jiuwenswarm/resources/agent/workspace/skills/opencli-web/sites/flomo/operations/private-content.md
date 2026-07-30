# Flomo: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `memos` | `private_content_read` / `medium` | `opencli flomo memos [--limit <limit>] [--since <since>] [--slug "<slug>"] -f json`<br>List your Flomo memos | `limit` (int, optional, default=20, minimum=1,maximum=200); `since` (int, optional, minimum=0); `slug` (str, optional, pattern=^[A-Za-z0-9_-]{1,256}$) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `memos`: Source-audited against OpenCLI 1.8.6 flomo/memos.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private memo content, account identifiers
