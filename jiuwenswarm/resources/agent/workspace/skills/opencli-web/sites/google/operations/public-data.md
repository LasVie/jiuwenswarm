# Google: public-data

Read low-risk public data without browser state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `news` | `public_read` / `low` | `opencli google news ["<keyword>"] [--limit <limit>] [--lang "<lang>"] [--region "<region>"] -f json`<br>Get Google News headlines | `keyword` (str, optional, positional); `limit` (int, optional, default=10, minimum=1,maximum=100); `lang` (str, optional, default='en', pattern=^[A-Za-z]{2,3}(?:-[A-Za-z0-9]+)?$); `region` (str, optional, default='US', pattern=^[A-Z]{2}$) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `suggest` | `public_read` / `low` | `opencli google suggest "<keyword>" [--lang "<lang>"] -f json`<br>Get Google search suggestions | `keyword` (str, required, positional); `lang` (str, optional, default='zh-CN') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `trends` | `public_read` / `low` | `opencli google trends [--region "<region>"] [--limit <limit>] -f json`<br>Get Google Trends daily trending searches | `region` (str, optional, default='US', pattern=^[A-Z]{2}$); `limit` (int, optional, default=20, minimum=1,maximum=100) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
