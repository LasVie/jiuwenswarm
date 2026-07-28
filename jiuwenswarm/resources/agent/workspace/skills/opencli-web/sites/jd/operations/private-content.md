---
opencli_contract:
  version: 2
  site: jd
  operation: private-content
  policy_sha256: fce05c10acfc834da9082a6dc11ff08ad5011c94960640d9163b78e3e643a122
  commands:
    cart:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    detail:
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
      - help: 商品 SKU ID
        name: sku
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
    item:
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    reviews:
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
      - help: 搜索关键词
        name: query
        positional: true
        required: true
        type: str
      - default: 10
        help: 返回结果数量 (max 30)
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

# Jd: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `cart` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>查看京东购物车 | none |
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>京东商品详情 | `sku` (str, required, positional) |
| `item` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>京东商品详情（价格、店铺、规格参数、主图、详情图） | `sku` (str, required, positional); `images` (int, optional, default=200) |
| `reviews` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>京东商品评价 | `sku` (str, required, positional); `limit` (int, optional, default=10) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>京东商品搜索 | `query` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
