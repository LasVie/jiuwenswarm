# Openfda

- Site slug: `openfda`
- Domains: `fda.gov`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `drug-label`, `food-recall` | `sites/openfda/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `drug-label` | `public_read` / `low` | `opencli openfda drug-label "<query>" [--limit <limit>] -f json`<br>Search FDA-approved drug labels (brand or generic name) | `query` (str, required, positional); `limit` (int, optional, default=5) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `food-recall` | `public_read` / `low` | `opencli openfda food-recall [--query "<query>"] [--status "<status>"] [--classification "<classification>"] [--limit <limit>] -f json`<br>FDA food recall and enforcement actions (most recent first) | `query` (str, optional); `status` (str, optional); `classification` (str, optional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
