# V2Ex: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `hot` | `public_read` / `low` | `opencli v2ex hot [--limit <limit>] -f json`<br>V2EX 热门话题 | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `latest` | `public_read` / `low` | `opencli v2ex latest [--limit <limit>] -f json`<br>V2EX 最新话题 | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `member` | `public_read` / `low` | `opencli v2ex member "<username>" -f json`<br>V2EX 用户资料 | `username` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `node` | `public_read` / `low` | `opencli v2ex node "<name>" [--limit <limit>] -f json`<br>V2EX 节点话题列表 | `name` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `nodes` | `public_read` / `low` | `opencli v2ex nodes [--limit <limit>] -f json`<br>V2EX 所有节点列表 | `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `replies` | `public_read` / `low` | `opencli v2ex replies "<id>" [--limit <limit>] -f json`<br>V2EX 主题回复列表 | `id` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `topic` | `public_read` / `low` | `opencli v2ex topic "<id>" -f json`<br>V2EX 主题详情和回复 | `id` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli v2ex user "<username>" [--limit <limit>] -f json`<br>V2EX 用户发帖列表 | `username` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
