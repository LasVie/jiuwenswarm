# Kimi: account

Read account identity or account-scoped metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `account` | `private_account_read` / `medium` | `opencli kimi account -f json`<br>Read account info from the Kimi sidebar (display name + plan label, e.g. "Allegretto"). | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `cookies` | `private_account_read` / `high` | `opencli kimi cookies -f json`<br>List kimi.com cookies visible to JavaScript (httpOnly cookies are deliberately not shown). | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `idb-list` | `private_account_read` / `medium` | `opencli kimi idb-list -f json`<br>List IndexedDB databases on kimi.com. | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `status` | `private_account_read` / `medium` | `opencli kimi status -f json`<br>Check Kimi page connection, login state, and current URL. | none | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `storage-get` | `private_account_read` / `high` | `opencli kimi storage-get "<key>" [--storage "<storage>"] [--max-bytes <max-bytes>] -f json`<br>Read a single localStorage / sessionStorage value on kimi.com. Auto-decodes JSON. | `key` (str, required, positional); `storage` (str, optional, default='local'); `max-bytes` (int, optional, default=4000) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `storage-keys` | `private_account_read` / `high` | `opencli kimi storage-keys [--storage "<storage>"] [--filter "<filter>"] [--limit <limit>] -f json`<br>List localStorage / sessionStorage keys on kimi.com (with byte sizes). | `storage` (str, optional, default='local'); `filter` (str, optional); `limit` (int, optional, default=100) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `usage` | `private_account_read` / `medium` | `opencli kimi usage -f json`<br>Read Kimi membership quota usage from the subscription page: total usage, rate limits, gift quota, and booster balance. | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `whoami` | `private_account_read` / `medium` | `opencli kimi whoami -f json`<br>Show the current logged-in kimi account | none | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `account`: Source-audited against OpenCLI 1.8.6 kimi/ui.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
- `cookies`: Source-audited against OpenCLI 1.8.6 kimi/storage.js; reads raw browser-session storage or cookie metadata and can expose authentication-adjacent values.; sensitive output: browser cookies, account identifiers
- `idb-list`: Source-audited against OpenCLI 1.8.6 kimi/storage.js; reads raw browser-session storage or cookie metadata and can expose authentication-adjacent values.; sensitive output: browser storage metadata, account identifiers
- `status`: Source-audited against OpenCLI 1.8.6 kimi/chat.js; reads current browser-session authentication state without changing it.; sensitive output: authentication state
- `storage-get`: Source-audited against OpenCLI 1.8.6 kimi/storage.js; reads raw browser-session storage or cookie metadata and can expose authentication-adjacent values.; sensitive output: browser storage values, account identifiers
- `storage-keys`: Source-audited against OpenCLI 1.8.6 kimi/storage.js; reads raw browser-session storage or cookie metadata and can expose authentication-adjacent values.; sensitive output: browser storage metadata, account identifiers
- `usage`: Source-audited against OpenCLI 1.8.6 kimi/usage.js; reads current browser-session or account-scoped metadata.; sensitive output: subscription and quota data, account identifiers
- `whoami`: Source-audited against OpenCLI 1.8.6 kimi/auth.js; reads current browser-session or account-scoped metadata.; sensitive output: account identifiers
