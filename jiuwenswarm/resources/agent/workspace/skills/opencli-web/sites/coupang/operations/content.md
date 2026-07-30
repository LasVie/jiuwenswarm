# Coupang: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `product` | `public_read` / `low` | `opencli coupang product ["<product-id>"] [--url "<url>"] -f json`<br>Read full product detail (price, rating, seller, delivery) for a Coupang product | `product-id` (str, optional, positional); `url` (str, optional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `product`: Source-audited against OpenCLI 1.8.6 coupang/product.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
