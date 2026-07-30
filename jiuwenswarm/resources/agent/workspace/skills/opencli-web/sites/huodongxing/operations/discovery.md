# Huodongxing: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `events` | `public_read` / `low` | `opencli huodongxing events [--tag "<tag>"] [--city "<city>"] [--date "<date>"] [--dateTo "<dateTo>"] [--eventType <eventType>] [--qs "<qs>"] [--limit <limit>] -f json`<br>活动行活动搜索（按标签、城市、日期、线上/线下、名称过滤） | `tag` (string, optional, default=''); `city` (string, optional, default='全部'); `date` (string, optional, default=''); `dateTo` (string, optional, default=''); `eventType` (int, optional); `qs` (string, optional, default=''); `limit` (int, optional, default=20) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `events`: Source-audited against OpenCLI 1.8.6 huodongxing/events.js; reads public browser-rendered content without authenticated account state.
