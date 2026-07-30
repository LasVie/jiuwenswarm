# Sinafinance: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `stock` | `public_read` / `low` | `opencli sinafinance stock "<key>" [--market "<market>"] -f json`<br>新浪财经行情（A股/港股/美股） | `key` (string, required, positional); `market` (string, optional, default='auto') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `stock`: Market-data read only; no trading authority and not investment advice.
