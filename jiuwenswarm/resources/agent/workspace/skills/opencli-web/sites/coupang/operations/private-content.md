---
opencli_contract:
  version: 2
  site: coupang
  operation: private-content
  policy_sha256: fabb4365f754060a5bc82634e522f0478a6d7f49e63addf6b3fb44a03ddd6a77
  commands:
    product:
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
      - help: Coupang product ID (digits only)
        name: product-id
        positional: true
        required: false
        type: str
      - help: Canonical Coupang product URL (alternative to --product-id)
        name: url
        required: false
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
    search:
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
      - help: Search keyword
        name: query
        positional: true
        required: true
        type: str
      - default: 1
        help: Search result page number
        name: page
        required: false
        type: int
      - default: 20
        help: Max results (max 50)
        name: limit
        required: false
        type: int
      - help: 'Optional search filter (currently supports: rocket)'
        name: filter
        required: false
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

# Coupang: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `product` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read full product detail (price, rating, seller, delivery) for a Coupang product | `product-id` (str, optional, positional); `url` (str, optional) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search Coupang products with logged-in browser session | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20); `filter` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
