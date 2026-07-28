---
opencli_contract:
  version: 2
  site: amazon
  operation: private-content
  policy_sha256: 22dbfaf2cb0e7d6c23d60914de971b805c8df34a2f3a448265d87a2a388ecb8e
  commands:
    bestsellers:
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
      - help: Ranking URL or supported Amazon path. Omit to use the list root.
        name: input
        positional: true
        required: false
        type: str
      - default: 100
        help: Maximum number of ranked items to return (default 100)
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
    discussion:
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
      - help: ASIN or product URL, for example B0FJS72893
        name: input
        positional: true
        required: true
        type: str
      - default: 10
        help: Maximum number of review samples to return (default 10)
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
    movers-shakers:
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
      - help: Ranking URL or supported Amazon path. Omit to use the list root.
        name: input
        positional: true
        required: false
        type: str
      - default: 100
        help: Maximum number of ranked items to return (default 100)
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
    offer:
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
      - help: ASIN or product URL, for example B0FJS72893
        name: input
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
      - help: ASIN or product URL, for example B0FJS72893
        name: input
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
      - help: Search query, for example "desk shelf organizer"
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Maximum number of results to return (default 20)
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
---

# Amazon: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `bestsellers` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Amazon Best Sellers pages for category candidate discovery | `input` (str, optional, positional); `limit` (int, optional, default=100) |
| `discussion` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Amazon review summary and sample customer discussion from product review pages | `input` (str, required, positional); `limit` (int, optional, default=10) |
| `movers-shakers` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Amazon Movers & Shakers pages for short-term growth signals | `input` (str, optional, positional); `limit` (int, optional, default=100) |
| `offer` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Amazon seller, buy box, and fulfillment facts from the product page | `input` (str, required, positional) |
| `product` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Amazon product page facts for candidate validation | `input` (str, required, positional) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Amazon search results for product discovery and coarse filtering | `query` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
