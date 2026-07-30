# Eastmoney: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `announcement` | `public_read` / `low` | `opencli eastmoney announcement [--market "<market>"] [--limit <limit>] -f json`<br>上市公司公告（按交易所筛选） | `market` (string, optional, default='SHA,SZA,BJA'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `convertible` | `public_read` / `low` | `opencli eastmoney convertible [--sort "<sort>"] [--limit <limit>] -f json`<br>可转债行情列表（默认按成交额排序） | `sort` (string, optional, default='turnover'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `etf` | `public_read` / `low` | `opencli eastmoney etf [--sort "<sort>"] [--limit <limit>] -f json`<br>ETF 列表按成交额/涨跌幅排行 | `sort` (string, optional, default='turnover'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `holders` | `public_read` / `low` | `opencli eastmoney holders "<symbol>" [--limit <limit>] -f json`<br>十大流通股东（A股 F10 数据） | `symbol` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `index-board` | `public_read` / `low` | `opencli eastmoney index-board [--group "<group>"] -f json`<br>主要市场指数行情（A股 / 港股 / 美股） | `group` (string, optional, default='main') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `kline` | `public_read` / `low` | `opencli eastmoney kline "<symbol>" [--period "<period>"] [--adjust "<adjust>"] [--limit <limit>] -f json`<br>K线历史数据（分/日/周/月/前复权/后复权） | `symbol` (str, required, positional); `period` (string, optional, default='day'); `adjust` (string, optional, default='forward'); `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `kuaixun` | `public_read` / `low` | `opencli eastmoney kuaixun [--column "<column>"] [--limit <limit>] -f json`<br>东方财富 7x24 财经快讯 | `column` (string, optional, default='102'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `longhu` | `public_read` / `low` | `opencli eastmoney longhu [--date "<date>"] [--limit <limit>] -f json`<br>龙虎榜明细（A股交易所公开披露榜单） | `date` (string, optional, default=''); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `money-flow` | `public_read` / `low` | `opencli eastmoney money-flow [--range "<range>"] [--order "<order>"] [--limit <limit>] -f json`<br>主力资金净流入排行（今日/5日/10日） | `range` (string, optional, default='today'); `order` (string, optional, default='desc'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `northbound` | `public_read` / `low` | `opencli eastmoney northbound [--direction "<direction>"] [--limit <limit>] -f json`<br>沪深港通北向/南向资金当日分时净流入（万元） | `direction` (string, optional, default='north'); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `quote` | `public_read` / `low` | `opencli eastmoney quote "<symbols>" -f json`<br>个股实时行情（A股 / 港股 / 美股）— 来自 push2.eastmoney.com | `symbols` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `rank` | `public_read` / `low` | `opencli eastmoney rank [--market "<market>"] [--sort "<sort>"] [--limit <limit>] -f json`<br>东财市场涨跌/成交排行（沪深/北证/创/科/港/美） | `market` (string, optional, default='hs-a'); `sort` (string, optional, default='change'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `sectors` | `public_read` / `low` | `opencli eastmoney sectors [--type "<type>"] [--sort "<sort>"] [--limit <limit>] -f json`<br>板块排行（行业/概念/地域）按涨跌幅、主力资金或成交额排序 | `type` (string, optional, default='industry'); `sort` (string, optional, default='change'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `announcement`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `convertible`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `etf`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `holders`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `index-board`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `kline`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `kuaixun`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `longhu`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `money-flow`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `northbound`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `quote`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `rank`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
- `sectors`: Read-only market/reference data; must never place orders, trade, or transact; not investment advice.
