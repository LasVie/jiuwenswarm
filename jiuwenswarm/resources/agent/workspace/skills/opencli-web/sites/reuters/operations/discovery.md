# Reuters: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli reuters search "<query>" [--limit <limit>] -f json`<br>Reuters 路透社新闻搜索 | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 reuters/search.js; reads Reuters content visible in the current browser session and does not bypass login, subscription, paywall, or human-verification controls.
