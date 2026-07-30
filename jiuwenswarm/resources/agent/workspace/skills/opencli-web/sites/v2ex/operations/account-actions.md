# V2Ex: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `daily` | `reversible_remote_write` / `high` | `opencli v2ex daily -f json`<br>V2EX 每日签到并领取铜币 | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
