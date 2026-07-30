# Facebook: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `private_content_read` / `medium` | `opencli facebook feed [--limit <limit>] -f json`<br>Get your Facebook news feed | `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `friends` | `private_content_read` / `medium` | `opencli facebook friends [--limit <limit>] -f json`<br>Get Facebook friend suggestions | `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `groups` | `private_content_read` / `medium` | `opencli facebook groups [--limit <limit>] -f json`<br>List your Facebook groups | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `marketplace-inbox` | `private_content_read` / `medium` | `opencli facebook marketplace-inbox [--limit <limit>] -f json`<br>List recent Facebook Marketplace buyer/seller conversations | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `marketplace-listings` | `private_content_read` / `medium` | `opencli facebook marketplace-listings [--limit <limit>] -f json`<br>List your Facebook Marketplace seller listings | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `memories` | `private_content_read` / `medium` | `opencli facebook memories [--limit <limit>] -f json`<br>Get your Facebook memories (On This Day) | `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notifications` | `private_content_read` / `medium` | `opencli facebook notifications [--limit <limit>] -f json`<br>Get recent Facebook notifications (含 unread / time / url / notif_id / notif_type 列) | `limit` (int, optional, default=15) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `feed`: sensitive output: private content, account identifiers
- `friends`: sensitive output: private content, account identifiers
- `groups`: sensitive output: private content, account identifiers
- `marketplace-inbox`: sensitive output: private content, account identifiers
- `marketplace-listings`: sensitive output: private content, account identifiers
- `memories`: sensitive output: private content, account identifiers
- `notifications`: sensitive output: private content, account identifiers
