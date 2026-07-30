# Coupang: account-actions

Change reversible account relationship or saved state.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `add-to-cart` | `reversible_remote_write` / `high` | `opencli coupang add-to-cart ["<product-id>"] [--url "<url>"] -f json`<br>Add a Coupang product to cart using logged-in browser session | `product-id` (str, optional, positional); `url` (str, optional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
