# Pixiv: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `detail` | `public_read` / `low` | `opencli pixiv detail "<id>" -f json`<br>View illustration details (tags, stats, URLs) | `id` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli pixiv user "<uid>" -f json`<br>View Pixiv artist profile | `uid` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 pixiv/detail.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user`: Source-audited against OpenCLI 1.8.6 pixiv/user.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
