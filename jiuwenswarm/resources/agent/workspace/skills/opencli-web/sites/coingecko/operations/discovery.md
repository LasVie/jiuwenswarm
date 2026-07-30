# Coingecko: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `categories` | `public_read` / `low` | `opencli coingecko categories [--sort "<sort>"] [--limit <limit>] -f json`<br>Crypto categories ranked by aggregated market cap | `sort` (str, optional, default='market_cap_desc'); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `trending` | `public_read` / `low` | `opencli coingecko trending -f json`<br>Top trending cryptocurrencies on CoinGecko in the last 24h (search-volume based). | none | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `categories`: Market-data read only; no trading authority and not investment advice.
- `trending`: Market-data read only; no trading authority and not investment advice.
