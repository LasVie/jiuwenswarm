# Defillama

- Site slug: `defillama`
- Domains: `defillama.com`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `protocol`, `protocols` | `sites/defillama/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `protocol` | `public_read` / `low` | `opencli defillama protocol "<slug>" -f json`<br>Single DefiLlama protocol details (current TVL, mcap, chains, twitter, github, description) | `slug` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `protocols` | `public_read` / `low` | `opencli defillama protocols [--limit <limit>] -f json`<br>Top DeFi protocols on DefiLlama by current TVL (slug, name, category, TVL, mcap, change_1d/7d, chains) | `limit` (int, optional, default=30) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `protocol`: Protocol and market data read only; no transaction authority and not investment advice.
- `protocols`: Protocol and market data read only; no transaction authority and not investment advice.
