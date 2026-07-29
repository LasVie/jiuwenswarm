---
opencli_contract:
  version: 2
  site: coupang
  operation: content
  policy_sha256: 15c9c239b0ba09eff87a1bba06361a2c5302d3e26fe8bbdf0afc9cea0984cb15
  commands:
    product:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Coupang: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `product` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read full product detail (price, rating, seller, delivery) for a Coupang product | `product-id` (str, optional, positional); `url` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
