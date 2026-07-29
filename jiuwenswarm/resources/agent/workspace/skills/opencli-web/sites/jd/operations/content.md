---
opencli_contract:
  version: 2
  site: jd
  operation: content
  policy_sha256: c50ca26ce20d4fdc7cb32d0e4930d9ef74069f8057059acb06c45d3311c2cf09
  commands:
    detail:
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
      - help: 商品 SKU ID
        name: sku
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    item:
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
      - help: 商品 SKU ID（如 100291143898）
        name: sku
        positional: true
        required: true
        type: str
      - default: 200
        help: 图片数量上限（默认200）
        name: images
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    reviews:
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
      - help: 商品 SKU ID
        name: sku
        positional: true
        required: true
        type: str
      - default: 10
        help: 返回评价数量 (max 20)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Jd: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `detail` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>京东商品详情 | `sku` (str, required, positional) |
| `item` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>京东商品详情（价格、店铺、规格参数、主图、详情图） | `sku` (str, required, positional); `images` (int, optional, default=200) |
| `reviews` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>京东商品评价 | `sku` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
