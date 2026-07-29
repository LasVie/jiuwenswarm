---
opencli_contract:
  version: 2
  site: amazon
  operation: content
  policy_sha256: d829909e04280195a5861590061a9e1f4c71232378a0219b70dc6d18da50fe38
  commands:
    discussion:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      sensitive_output: []
    offer:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      sensitive_output: []
    product:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      sensitive_output: []
---

# Amazon: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `discussion` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Amazon review summary and sample customer discussion from product review pages | `input` (str, required, positional); `limit` (int, optional, default=10) |
| `offer` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Amazon seller, buy box, and fulfillment facts from the product page | `input` (str, required, positional) |
| `product` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Amazon product page facts for candidate validation | `input` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
