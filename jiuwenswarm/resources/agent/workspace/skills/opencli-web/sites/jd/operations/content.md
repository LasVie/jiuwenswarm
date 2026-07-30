# Jd: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `public_read` / `low` | `opencli jd detail "<sku>" -f json`<br>京东商品详情 | `sku` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `item` | `public_read` / `low` | `opencli jd item "<sku>" [--images <images>] -f json`<br>京东商品详情（价格、店铺、规格参数、主图、详情图） | `sku` (str, required, positional); `images` (int, optional, default=200) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `reviews` | `public_read` / `low` | `opencli jd reviews "<sku>" [--limit <limit>] -f json`<br>京东商品评价 | `sku` (str, required, positional); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 jd/detail.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `item`: Source-audited against OpenCLI 1.8.6 jd/item.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `reviews`: Source-audited against OpenCLI 1.8.6 jd/reviews.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
