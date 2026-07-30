# Dianping: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `shop` | `public_read` / `low` | `opencli dianping shop "<shop_id>" -f json`<br>大众点评店铺详情（按 shop_id） | `shop_id` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `shop`: Source-audited against OpenCLI 1.8.6 dianping/shop.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
