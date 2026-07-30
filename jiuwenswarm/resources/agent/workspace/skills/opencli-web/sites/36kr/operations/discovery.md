# 36Kr: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli 36kr hot [--limit <limit>] [--type "<type>"] -f json`<br>36氪热榜 — trending articles (renqi/zonghe/shoucang/catalog) | `limit` (int, optional, default=20); `type` (string, optional, default='catalog') | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `news` | `public_read` / `low` | `opencli 36kr news [--limit <limit>] -f json`<br>Latest tech/startup news from 36kr (36氪) | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli 36kr search "<query>" [--limit <limit>] -f json`<br>搜索36氪文章 | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `hot`: Source-audited against OpenCLI 1.8.6 36kr/hot.js; reads public browser-rendered content without authenticated account state.
- `search`: Source-audited against OpenCLI 1.8.6 36kr/search.js; reads public browser-rendered content without authenticated account state.
