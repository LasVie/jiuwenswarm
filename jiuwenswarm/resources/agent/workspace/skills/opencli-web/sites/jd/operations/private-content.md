# Jd: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `cart` | `private_content_read` / `medium` | `opencli jd cart -f json`<br>查看京东购物车 | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `cart`: Source-audited against OpenCLI 1.8.6 jd/cart.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: shopping cart contents, account identifiers
