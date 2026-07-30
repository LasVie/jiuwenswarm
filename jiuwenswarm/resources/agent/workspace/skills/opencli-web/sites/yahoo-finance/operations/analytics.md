# Yahoo Finance: analytics

Read aggregate metrics, trends, or rankings.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `quote` | `public_read` / `low` | `opencli yahoo-finance quote "<symbol>" -f json`<br>Yahoo Finance 股票行情 | `symbol` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `quote`: Source-audited against OpenCLI 1.8.6 yahoo-finance/quote.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
