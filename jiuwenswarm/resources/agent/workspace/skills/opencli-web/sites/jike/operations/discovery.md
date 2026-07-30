# Jike: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli jike search "<query>" [--limit <limit>] -f json`<br>搜索即刻帖子 | `query` (string, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 jike/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
