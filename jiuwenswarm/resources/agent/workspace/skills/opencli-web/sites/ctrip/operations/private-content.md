# Ctrip: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `attraction` | `private_content_read` / `medium` | `opencli ctrip attraction "<city>" [--limit "<limit>"] -f json`<br>列出携程某城市的热门景点（评分/点评数，城市 id 经 ctrip search 获取） | `city` (str, required, positional); `limit` (str, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `bus` | `private_content_read` / `medium` | `opencli ctrip bus "<from>" "<to>" --date "<date>" [--limit "<limit>"] -f json`<br>搜索携程汽车票（按出发/到达城市名 + 日期） | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (str, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `cruise` | `private_content_read` / `medium` | `opencli ctrip cruise "<port>" [--limit "<limit>"] -f json`<br>搜索携程邮轮线路（按出发港名） | `port` (str, required, positional); `limit` (str, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `ferry` | `private_content_read` / `medium` | `opencli ctrip ferry "<from>" "<to>" --date "<date>" [--limit "<limit>"] -f json`<br>搜索携程船票（按出发/到达城市名 + 日期） | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (str, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `flight-round` | `private_content_read` / `medium` | `opencli ctrip flight-round "<from>" "<to>" --depart "<depart>" --return "<return>" [--limit "<limit>"] -f json`<br>搜索携程往返机票（按出发/到达 IATA 三字码 + 去/返日期，返回去程腿含往返总价） | `from` (str, required, positional); `to` (str, required, positional); `depart` (str, required); `return` (str, required); `limit` (str, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `hotel` | `private_content_read` / `medium` | `opencli ctrip hotel "<id>" -f json`<br>查看携程单个酒店详情（评分细分、热门设施、入离政策、位置） | `id` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `package` | `private_content_read` / `medium` | `opencli ctrip package "<destination>" [--limit "<limit>"] -f json`<br>搜索携程机+酒自由行套餐（按目的地关键词） | `destination` (str, required, positional); `limit` (str, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `tour` | `private_content_read` / `medium` | `opencli ctrip tour "<destination>" [--limit "<limit>"] -f json`<br>搜索携程旅游线路（按目的地关键词，跟团/自由行） | `destination` (str, required, positional); `limit` (str, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `train` | `private_content_read` / `medium` | `opencli ctrip train "<from>" "<to>" --date "<date>" [--limit "<limit>"] -f json`<br>搜索携程火车票（按出发/到达站名 + 日期） | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (str, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `attraction`: sensitive output: private content, account identifiers
- `bus`: sensitive output: private content, account identifiers
- `cruise`: sensitive output: private content, account identifiers
- `ferry`: sensitive output: private content, account identifiers
- `flight-round`: sensitive output: private content, account identifiers
- `hotel`: sensitive output: private content, account identifiers
- `package`: sensitive output: private content, account identifiers
- `tour`: sensitive output: private content, account identifiers
- `train`: sensitive output: private content, account identifiers
