---
opencli_contract:
  version: 2
  site: coupang
  operation: account-actions
  policy_sha256: 15c9c239b0ba09eff87a1bba06361a2c5302d3e26fe8bbdf0afc9cea0984cb15
  commands:
    add-to-cart:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Coupang product ID
        name: product-id
        positional: true
        required: false
        type: str
      - help: Canonical product URL
        name: url
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Coupang: account-actions

Change reversible account relationship or saved state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `add-to-cart` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Add a Coupang product to cart using logged-in browser session | `product-id` (str, optional, positional); `url` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
