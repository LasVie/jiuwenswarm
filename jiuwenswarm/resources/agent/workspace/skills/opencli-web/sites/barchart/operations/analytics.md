# Barchart: analytics

Read aggregate metrics, trends, or rankings.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `flow` | `public_read` / `low` | `opencli barchart flow [--type "<all\|call\|put>"] [--limit <limit>] -f json`<br>Barchart unusual options activity / options flow | `type` (str, optional, default='all', choices=all,call,put); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `greeks` | `public_read` / `low` | `opencli barchart greeks "<symbol>" [--expiration "<expiration>"] [--limit <limit>] -f json`<br>Barchart options greeks overview (IV, delta, gamma, theta, vega) | `symbol` (str, required, positional); `expiration` (str, optional); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `options` | `public_read` / `low` | `opencli barchart options "<symbol>" [--type "<Call\|Put>"] [--limit <limit>] -f json`<br>Barchart options chain with greeks, IV, volume, and open interest | `symbol` (str, required, positional); `type` (str, optional, default='Call', choices=Call,Put); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `quote` | `public_read` / `low` | `opencli barchart quote "<symbol>" -f json`<br>Barchart stock quote with price, volume, and key metrics | `symbol` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `flow`: Source-audited against OpenCLI 1.8.6 barchart/flow.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `greeks`: Source-audited against OpenCLI 1.8.6 barchart/greeks.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `options`: Source-audited against OpenCLI 1.8.6 barchart/options.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `quote`: Source-audited against OpenCLI 1.8.6 barchart/quote.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
