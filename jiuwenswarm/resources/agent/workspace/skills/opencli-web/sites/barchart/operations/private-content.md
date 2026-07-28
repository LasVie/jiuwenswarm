---
opencli_contract:
  version: 2
  site: barchart
  operation: private-content
  policy_sha256: 402e5bf511841250dbfbc9c150dca1e5924cc9b556a75d2666eb70fe8ef56633
  commands:
    flow:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - choices:
        - all
        - call
        - put
        default: all
        help: 'Filter: all, call, or put'
        name: type
        required: false
        type: str
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    greeks:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Stock ticker (e.g. AAPL)
        name: symbol
        positional: true
        required: true
        type: str
      - help: Expiration date (YYYY-MM-DD). Defaults to the nearest available expiration.
        name: expiration
        required: false
        type: str
      - default: 10
        help: Number of near-the-money strikes per type (1-100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    options:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Stock ticker (e.g. AAPL)
        name: symbol
        positional: true
        required: true
        type: str
      - choices:
        - Call
        - Put
        default: Call
        help: 'Option type: Call or Put'
        name: type
        required: false
        type: str
      - default: 20
        help: Max number of strikes to return
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    quote:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Stock ticker (e.g. AAPL, MSFT, TSLA)
        name: symbol
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Barchart: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `flow` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Barchart unusual options activity / options flow | `type` (str, optional, default='all', choices=all,call,put); `limit` (int, optional, default=20) |
| `greeks` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Barchart options greeks overview (IV, delta, gamma, theta, vega) | `symbol` (str, required, positional); `expiration` (str, optional); `limit` (int, optional, default=10) |
| `options` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Barchart options chain with greeks, IV, volume, and open interest | `symbol` (str, required, positional); `type` (str, optional, default='Call', choices=Call,Put); `limit` (int, optional, default=20) |
| `quote` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Barchart stock quote with price, volume, and key metrics | `symbol` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
