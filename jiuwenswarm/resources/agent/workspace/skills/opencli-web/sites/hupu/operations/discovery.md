# Hupu: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli hupu hot [--limit <limit>] -f json`<br>虎扑首页热门帖子（含 lights / replies / forum / is_hot 列） | `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli hupu search "<query>" [--page <page>] [--limit <limit>] [--forum "<forum>"] [--sort "<sort>"] -f json`<br>搜索虎扑帖子 (使用官方API) | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20); `forum` (str, optional); `sort` (str, optional, default='general') | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `hot`: Source-audited against OpenCLI 1.8.6 hupu/hot.js; reads public browser-rendered content without authenticated account state.
- `search`: Source-audited against OpenCLI 1.8.6 hupu/search.js; reads public browser-rendered content without authenticated account state.
