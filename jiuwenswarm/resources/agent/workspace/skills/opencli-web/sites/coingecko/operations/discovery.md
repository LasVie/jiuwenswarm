---
opencli_contract:
  version: 2
  site: coingecko
  operation: discovery
  policy_sha256: 9cef157f641dae49bbcee4919fcffee86a226317729d2987588f33b53769feab
  commands:
    categories:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: market_cap_desc
        help: Sort order (market_cap_desc / market_cap_asc / name_desc / name_asc / market_cap_change_24h_desc / market_cap_change_24h_asc)
        name: sort
        required: false
        type: str
      - default: 20
        help: Number of categories (1-100; CoinGecko returns ~120 max)
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    trending:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Coingecko: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `categories` | `enabled` | `public_read` / `low` | `opencli_execute(site="coingecko", operation="discovery", command="categories")`<br>Crypto categories ranked by aggregated market cap | `sort` (str, optional, default='market_cap_desc'); `limit` (int, optional, default=20) |
| `trending` | `enabled` | `public_read` / `low` | `opencli_execute(site="coingecko", operation="discovery", command="trending")`<br>Top trending cryptocurrencies on CoinGecko in the last 24h (search-volume based). | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
