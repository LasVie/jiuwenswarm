# Weixin: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `drafts` | `private_content_read` / `medium` | `opencli weixin drafts [--limit <limit>] [--timeout <timeout>] -f json`<br>列出微信公众号草稿箱 | `limit` (int, optional, default=10); `timeout` (int, optional, default=60) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `drafts`: sensitive output: private content, account identifiers
