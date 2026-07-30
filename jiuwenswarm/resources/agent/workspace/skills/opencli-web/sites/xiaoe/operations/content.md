# Xiaoe: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `public_read` / `low` | `opencli xiaoe detail "<url>" -f json`<br>小鹅通课程详情（名称、价格、学员数、店铺） | `url` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 xiaoe/detail.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
