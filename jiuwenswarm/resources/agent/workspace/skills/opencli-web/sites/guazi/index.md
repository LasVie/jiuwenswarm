# Guazi

- Site slug: `guazi`
- Domains: `m.guazi.com`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `browse`, `car` | `sites/guazi/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `browse` | `public_read` / `low` | `opencli guazi browse ["<city>"] [--limit <limit>] -f json`<br>瓜子二手车在售车源列表（按城市，含售价/首付/里程/年份） | `city` (str, optional, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `car` | `public_read` / `low` | `opencli guazi car "<clue_id>" -f json`<br>瓜子二手车车源详情（售价 / 上牌 / 里程 / 过户 / 配置 / 车况） | `clue_id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
