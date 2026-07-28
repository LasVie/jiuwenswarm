---
opencli_contract:
  version: 2
  site: coingecko
  operation: content
  policy_sha256: 9cef157f641dae49bbcee4919fcffee86a226317729d2987588f33b53769feab
  commands:
    coin:
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
      - help: CoinGecko coin id (lowercase, e.g. bitcoin / ethereum / solana).
        name: id
        positional: true
        required: true
        type: string
      - default: usd
        help: Quote currency (usd, cny, eur, jpy, ...).
        name: currency
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    derivatives:
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
      - default: 20
        help: Max rows to return (1-500; CoinGecko returns one large page).
        name: limit
        required: false
        type: int
      - help: Optional symbol substring filter (e.g. "BTC", "ETHUSDT").
        name: symbol
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    exchanges:
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
      - default: 20
        help: Number of exchanges (1-250, CoinGecko per_page upper bound)
        name: limit
        required: false
        type: int
      - default: 1
        help: Page number (1-based)
        name: page
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    global:
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
      - default: usd
        help: Quote currency for total market cap / volume (usd, cny, eur, jpy, ...)
        name: currency
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    top:
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
      - default: usd
        help: 计价币种 (usd / cny / eur / jpy ...)
        name: currency
        required: false
        type: string
      - default: 10
        help: 返回数量（默认 10，最多 250）
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
---

# Coingecko: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `coin` | `enabled` | `public_read` / `low` | `opencli_execute(site="coingecko", operation="content", command="coin", arguments={"id":"<id>"})`<br>Fetch a single cryptocurrency's market data by CoinGecko id (e.g. bitcoin, ethereum). | `id` (string, required, positional); `currency` (string, optional, default='usd') |
| `derivatives` | `enabled` | `public_read` / `low` | `opencli_execute(site="coingecko", operation="content", command="derivatives")`<br>Top crypto derivative (perpetual / futures) markets by 24h volume | `limit` (int, optional, default=20); `symbol` (string, optional) |
| `exchanges` | `enabled` | `public_read` / `low` | `opencli_execute(site="coingecko", operation="content", command="exchanges")`<br>Top crypto exchanges by 24h BTC trading volume | `limit` (int, optional, default=20); `page` (int, optional, default=1) |
| `global` | `enabled` | `public_read` / `low` | `opencli_execute(site="coingecko", operation="content", command="global")`<br>Aggregate crypto market stats: total market cap, volume, dominance | `currency` (string, optional, default='usd') |
| `top` | `enabled` | `public_read` / `low` | `opencli_execute(site="coingecko", operation="content", command="top")`<br>按市值排序的加密货币行情（默认 USD） | `currency` (string, optional, default='usd'); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
