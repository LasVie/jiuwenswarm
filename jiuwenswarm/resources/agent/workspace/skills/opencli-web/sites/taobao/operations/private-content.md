# Taobao: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `cart` | `private_content_read` / `medium` | `opencli taobao cart [--limit <limit>] -f json`<br>查看淘宝购物车 | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `cart`: Source-audited against OpenCLI 1.8.6 taobao/cart.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: shopping cart contents, account identifiers
