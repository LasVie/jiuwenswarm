# 1688: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli 1688 search "<query>" [--limit <limit>] -f json`<br>1688 商品搜索（结果候选、卖家链接、价格/MOQ/销量文本） | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 1688/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
