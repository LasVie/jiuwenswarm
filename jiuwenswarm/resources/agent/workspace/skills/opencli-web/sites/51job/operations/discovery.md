# 51Job: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli 51job hot [--area "<area>"] [--sort "<sort>"] [--page <page>] [--limit <limit>] -f json`<br>51job 推荐职位（按城市/行业/排序浏览） | `area` (string, optional, default='全国'); `sort` (string, optional, default='综合'); `page` (int, optional, default=1); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli 51job search "<keyword>" [--area "<area>"] [--salary "<salary>"] [--experience "<experience>"] [--degree "<degree>"] [--companyType "<companyType>"] [--companySize "<companySize>"] [--sort "<sort>"] [--page <page>] [--limit <limit>] -f json`<br>51job 前程无忧关键词职位搜索 | `keyword` (string, required, positional); `area` (string, optional, default='全国'); `salary` (string, optional, default=''); `experience` (string, optional, default=''); `degree` (string, optional, default=''); `companyType` (string, optional, default=''); `companySize` (string, optional, default=''); `sort` (string, optional, default='综合'); `page` (int, optional, default=1); `limit` (int, optional, default=20) | auth=none; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `hot`: Source-audited against OpenCLI 1.8.6 51job/hot.js; reads public browser-rendered content without authenticated account state.
- `search`: Source-audited against OpenCLI 1.8.6 51job/search.js; reads public browser-rendered content without authenticated account state.
