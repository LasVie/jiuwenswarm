# Boss: write-actions

Change remote service state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `batchgreet` | `reversible_remote_write` / `high` | `opencli boss batchgreet [--job-id "<job-id>"] [--limit <limit>] [--text "<text>"] -f json`<br>BOSS直聘批量向推荐候选人发送招呼 | `job-id` (str, optional, default=''); `limit` (int, optional, default=5); `text` (str, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `exchange` | `reversible_remote_write` / `high` | `opencli boss exchange "<uid>" [--type "<phone\|wechat>"] -f json`<br>BOSS直聘交换联系方式（请求手机/微信） | `uid` (str, required, positional); `type` (str, optional, default='phone', choices=phone,wechat) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `greet` | `reversible_remote_write` / `high` | `opencli boss greet "<uid>" --security-id "<security-id>" --job-id "<job-id>" [--text "<text>"] -f json`<br>BOSS直聘向新候选人发送招呼（开始聊天） | `uid` (str, required, positional); `security-id` (str, required); `job-id` (str, required); `text` (str, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `mark` | `reversible_remote_write` / `high` | `opencli boss mark "<uid>" --label "<label>" [--remove <true\|false>] -f json`<br>BOSS直聘给候选人添加标签 | `uid` (str, required, positional); `label` (str, required); `remove` (boolean, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
