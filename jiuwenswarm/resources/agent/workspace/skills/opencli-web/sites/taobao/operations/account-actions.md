# Taobao: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `add-cart` | `reversible_remote_write` / `high` | `opencli taobao add-cart "<id>" [--spec "<spec>"] [--dry-run <true\|false>] -f json`<br>淘宝加入购物车 | `id` (str, required, positional); `spec` (str, optional); `dry-run` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
