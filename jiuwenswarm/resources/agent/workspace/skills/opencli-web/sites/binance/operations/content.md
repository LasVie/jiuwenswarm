---
opencli_contract:
  version: 2
  site: binance
  operation: content
  policy_sha256: d169c2ab4b9953db200277e543c5a9660f8fb7c062fed5137251583b3691f8a7
  commands:
    asks:
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
      - help: Trading pair symbol (e.g. BTCUSDT, ETHUSDT)
        name: symbol
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of price levels (5, 10, 20, 50, 100)
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
    depth:
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
      - help: Trading pair symbol (e.g. BTCUSDT, ETHUSDT)
        name: symbol
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of price levels (5, 10, 20, 50, 100)
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
    gainers:
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
      - default: 10
        help: Number of trading pairs
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
    klines:
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
      - help: Trading pair symbol (e.g. BTCUSDT, ETHUSDT)
        name: symbol
        positional: true
        required: true
        type: str
      - default: 1d
        help: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, 1w, 1M)
        name: interval
        required: false
        type: str
      - default: 10
        help: Number of klines (max 1000)
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
    losers:
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
      - default: 10
        help: Number of trading pairs
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
    pairs:
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
        help: Number of trading pairs
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
    price:
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
      - help: Trading pair symbol (e.g. BTCUSDT, ETHUSDT)
        name: symbol
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    prices:
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
        help: Number of prices
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
    ticker:
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
        help: Number of tickers
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
      - default: 20
        help: Number of trading pairs
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
    trades:
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
      - help: Trading pair symbol (e.g. BTCUSDT, ETHUSDT)
        name: symbol
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of trades (max 1000)
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

# Binance: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `asks` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="asks", arguments={"symbol":"<symbol>"})`<br>Order book ask prices for a trading pair | `symbol` (str, required, positional); `limit` (int, optional, default=10) |
| `depth` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="depth", arguments={"symbol":"<symbol>"})`<br>Order book bid and ask prices for a trading pair | `symbol` (str, required, positional); `limit` (int, optional, default=10) |
| `gainers` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="gainers")`<br>Top gaining trading pairs by 24h price change | `limit` (int, optional, default=10) |
| `klines` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="klines", arguments={"symbol":"<symbol>"})`<br>Candlestick/kline data for a trading pair | `symbol` (str, required, positional); `interval` (str, optional, default='1d'); `limit` (int, optional, default=10) |
| `losers` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="losers")`<br>Top losing trading pairs by 24h price change | `limit` (int, optional, default=10) |
| `pairs` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="pairs")`<br>List active trading pairs on Binance | `limit` (int, optional, default=20) |
| `price` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="price", arguments={"symbol":"<symbol>"})`<br>Quick price check for a trading pair | `symbol` (str, required, positional) |
| `prices` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="prices")`<br>Latest prices for all trading pairs | `limit` (int, optional, default=20) |
| `ticker` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="ticker")`<br>24h ticker statistics for top trading pairs by volume | `limit` (int, optional, default=20) |
| `top` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="top")`<br>Top trading pairs by 24h volume on Binance | `limit` (int, optional, default=20) |
| `trades` | `enabled` | `public_read` / `low` | `opencli_execute(site="binance", operation="content", command="trades", arguments={"symbol":"<symbol>"})`<br>Recent trades for a trading pair | `symbol` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
