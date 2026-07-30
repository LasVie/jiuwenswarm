# Upwork: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `private_content_read` / `medium` | `opencli upwork feed ["<tab>"] [--limit <limit>] -f json`<br>Upwork personalized jobs feed (best-matches \| most-recent) — requires login | `tab` (str, optional, positional, default='best-matches'); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `feed`: Source-audited against OpenCLI 1.8.6 upwork/feed.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private job recommendations, account identifiers
