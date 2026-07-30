# Coingecko: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `coin` | `public_read` / `low` | `opencli coingecko coin "<id>" [--currency "<currency>"] -f json`<br>Fetch a single cryptocurrency's market data by CoinGecko id (e.g. bitcoin, ethereum). | `id` (string, required, positional); `currency` (string, optional, default='usd') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `derivatives` | `public_read` / `low` | `opencli coingecko derivatives [--limit <limit>] [--symbol "<symbol>"] -f json`<br>Top crypto derivative (perpetual / futures) markets by 24h volume | `limit` (int, optional, default=20); `symbol` (string, optional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `exchanges` | `public_read` / `low` | `opencli coingecko exchanges [--limit <limit>] [--page <page>] -f json`<br>Top crypto exchanges by 24h BTC trading volume | `limit` (int, optional, default=20); `page` (int, optional, default=1) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `global` | `public_read` / `low` | `opencli coingecko global [--currency "<currency>"] -f json`<br>Aggregate crypto market stats: total market cap, volume, dominance | `currency` (string, optional, default='usd') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top` | `public_read` / `low` | `opencli coingecko top [--currency "<currency>"] [--limit <limit>] -f json`<br>按市值排序的加密货币行情（默认 USD） | `currency` (string, optional, default='usd'); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `coin`: Market-data read only; no trading authority and not investment advice.
- `derivatives`: Market-data read only; no trading authority and not investment advice.
- `exchanges`: Market-data read only; no trading authority and not investment advice.
- `global`: Market-data read only; no trading authority and not investment advice.
- `top`: Market-data read only; no trading authority and not investment advice.
