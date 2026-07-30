# Taobao: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `public_read` / `low` | `opencli taobao detail "<id>" -f json`<br>淘宝商品详情 | `id` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `reviews` | `public_read` / `low` | `opencli taobao reviews "<id>" [--limit <limit>] -f json`<br>淘宝商品评价 | `id` (str, required, positional); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 taobao/detail.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `reviews`: Source-audited against OpenCLI 1.8.6 taobao/reviews.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
