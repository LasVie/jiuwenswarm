# Booking: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli booking search "<destination>" --checkin "<checkin>" --checkout "<checkout>" [--adults <adults>] [--rooms <rooms>] [--children <children>] [--currency "<currency>"] [--lang "<lang>"] [--limit <limit>] [--offset <offset>] -f json`<br>Search Booking.com hotels by destination and dates (server-rendered card scrape). | `destination` (str, required, positional); `checkin` (str, required); `checkout` (str, required); `adults` (int, optional, default=2); `rooms` (int, optional, default=1); `children` (int, optional, default=0); `currency` (str, optional); `lang` (str, optional); `limit` (int, optional, default=25); `offset` (int, optional, default=0) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 booking/search.js; reads public browser-rendered content without authenticated account state.
