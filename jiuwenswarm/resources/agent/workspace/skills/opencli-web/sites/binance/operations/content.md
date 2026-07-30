# Binance: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `asks` | `public_read` / `low` | `opencli binance asks "<symbol>" [--limit <limit>] -f json`<br>Order book ask prices for a trading pair | `symbol` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `depth` | `public_read` / `low` | `opencli binance depth "<symbol>" [--limit <limit>] -f json`<br>Order book bid and ask prices for a trading pair | `symbol` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `gainers` | `public_read` / `low` | `opencli binance gainers [--limit <limit>] -f json`<br>Top gaining trading pairs by 24h price change | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `klines` | `public_read` / `low` | `opencli binance klines "<symbol>" [--interval "<interval>"] [--limit <limit>] -f json`<br>Candlestick/kline data for a trading pair | `symbol` (str, required, positional); `interval` (str, optional, default='1d'); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `losers` | `public_read` / `low` | `opencli binance losers [--limit <limit>] -f json`<br>Top losing trading pairs by 24h price change | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `pairs` | `public_read` / `low` | `opencli binance pairs [--limit <limit>] -f json`<br>List active trading pairs on Binance | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `price` | `public_read` / `low` | `opencli binance price "<symbol>" -f json`<br>Quick price check for a trading pair | `symbol` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `prices` | `public_read` / `low` | `opencli binance prices [--limit <limit>] -f json`<br>Latest prices for all trading pairs | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `ticker` | `public_read` / `low` | `opencli binance ticker [--limit <limit>] -f json`<br>24h ticker statistics for top trading pairs by volume | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `top` | `public_read` / `low` | `opencli binance top [--limit <limit>] -f json`<br>Top trading pairs by 24h volume on Binance | `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `trades` | `public_read` / `low` | `opencli binance trades "<symbol>" [--limit <limit>] -f json`<br>Recent trades for a trading pair | `symbol` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `asks`: Market-data read only; no trading authority and not investment advice.
- `depth`: Market-data read only; no trading authority and not investment advice.
- `gainers`: Market-data read only; no trading authority and not investment advice.
- `klines`: Market-data read only; no trading authority and not investment advice.
- `losers`: Market-data read only; no trading authority and not investment advice.
- `pairs`: Market-data read only; no trading authority and not investment advice.
- `price`: Market-data read only; no trading authority and not investment advice.
- `prices`: Market-data read only; no trading authority and not investment advice.
- `ticker`: Market-data read only; no trading authority and not investment advice.
- `top`: Market-data read only; no trading authority and not investment advice.
- `trades`: Market-data read only; no trading authority and not investment advice.
