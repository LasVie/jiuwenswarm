# Mubu: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `doc` | `private_content_read` / `medium` | `opencli mubu doc "<id>" [--output "<output>"] -f json`<br>读取幕布文档内容（默认输出 Markdown，可用 --output text 输出纯文本） | `id` (str, required, positional); `output` (str, optional, default='md') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `docs` | `private_content_read` / `medium` | `opencli mubu docs [--folder "<folder>"] [--starred <true\|false>] [--limit <limit>] -f json`<br>列出幕布文档（默认根目录，--starred 查看快速访问列表） | `folder` (str, optional, default='0'); `starred` (bool, optional, default=False); `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notes` | `private_content_read` / `medium` | `opencli mubu notes [--list <true\|false>] [--date "<date>"] [--month "<month>"] [--year <year>] [--from "<from>"] [--to "<to>"] [--output "<output>"] -f json`<br>读取幕布速记（默认今天）。支持 --date/--month/--year/--from/--to 指定时间范围，--list 为概览模式（日期+条数）。 | `list` (bool, optional, default=False); `date` (str, optional); `month` (str, optional); `year` (int, optional); `from` (str, optional); `to` (str, optional); `output` (str, optional, default='md') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `recent` | `private_content_read` / `medium` | `opencli mubu recent [--limit <limit>] -f json`<br>最近编辑的幕布文档 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search` | `private_content_read` / `medium` | `opencli mubu search "<query>" [--limit <limit>] -f json`<br>全局搜索幕布文档和文件夹（标题+内容，服务端全量匹配）。结果含 type/id/name/path/hits/snippet 字段。 | `query` (str, required, positional); `limit` (int, optional, default=100) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `doc`: sensitive output: private content, account identifiers
- `docs`: sensitive output: private content, account identifiers
- `notes`: sensitive output: private content, account identifiers
- `recent`: sensitive output: private content, account identifiers
- `search`: sensitive output: private content, account identifiers
