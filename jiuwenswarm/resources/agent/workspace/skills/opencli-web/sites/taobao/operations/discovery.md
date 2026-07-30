# Taobao: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli taobao search "<query>" [--sort "<default\|sale\|price>"] [--limit <limit>] -f json`<br>淘宝商品搜索 | `query` (str, required, positional); `sort` (str, optional, default='default', choices=default,sale,price); `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 taobao/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
