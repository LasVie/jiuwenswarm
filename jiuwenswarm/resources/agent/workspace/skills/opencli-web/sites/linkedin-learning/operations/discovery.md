# Linkedin Learning: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli linkedin-learning search "<keywords>" [--limit <limit>] -f json`<br>Search LinkedIn Learning courses, videos, and learning paths by keyword | `keywords` (string, required, positional); `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 linkedin-learning/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
