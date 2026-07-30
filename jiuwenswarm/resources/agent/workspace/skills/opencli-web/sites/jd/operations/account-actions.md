# Jd: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `add-cart` | `reversible_remote_write` / `high` | `opencli jd add-cart "<sku>" [--num <num>] [--dry-run <true\|false>] -f json`<br>京东加入购物车 | `sku` (str, required, positional); `num` (int, optional, default=1); `dry-run` (bool, optional, default=False) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
