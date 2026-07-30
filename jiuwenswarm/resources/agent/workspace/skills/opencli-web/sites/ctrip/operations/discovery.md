# Ctrip: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `flight` | `public_read` / `low` | `opencli ctrip flight "<from>" "<to>" --date "<date>" [--limit <limit>] -f json`<br>搜索携程一程机票（按出发/到达 IATA 三字码 + 日期） | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `hotel-search` | `public_read` / `low` | `opencli ctrip hotel-search "<city>" --checkin "<checkin>" --checkout "<checkout>" [--limit <limit>] -f json`<br>搜索携程酒店列表（按城市 + 入住/离店日期） | `city` (str, required, positional); `checkin` (str, required); `checkout` (str, required); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `hotel-suggest` | `public_read` / `low` | `opencli ctrip hotel-suggest "<query>" [--limit <limit>] -f json`<br>搜索携程酒店上下文联想：城市、商圈、单酒店匹配 | `query` (str, required, positional); `limit` (int, optional, default=15) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli ctrip search "<query>" [--limit <limit>] -f json`<br>搜索携程目的地、景区、火车站和地标联想结果 | `query` (str, required, positional); `limit` (int, optional, default=15) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `flight`: Source-audited against OpenCLI 1.8.6 ctrip/flight.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `hotel-search`: Source-audited against OpenCLI 1.8.6 ctrip/hotel-search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
