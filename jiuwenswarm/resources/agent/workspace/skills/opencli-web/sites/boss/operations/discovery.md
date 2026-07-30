# Boss: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli boss search ["<query>"] [--city "<city>"] [--experience "<experience>"] [--degree "<degree>"] [--salary "<salary>"] [--industry "<industry>"] [--jobType "<jobType>"] [--page <page>] [--limit <limit>] -f json`<br>BOSS直聘搜索职位（不带关键词时返回为你推荐职位） | `query` (str, optional, positional); `city` (str, optional, default='北京'); `experience` (str, optional, default=''); `degree` (str, optional, default=''); `salary` (str, optional, default=''); `industry` (str, optional, default=''); `jobType` (str, optional, default=''); `page` (int, optional, default=1); `limit` (int, optional, default=15) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
