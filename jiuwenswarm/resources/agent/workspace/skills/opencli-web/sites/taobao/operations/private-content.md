---
opencli_contract:
  version: 2
  site: taobao
  operation: private-content
  policy_sha256: fcf528d2e79e281ffebd0783a0ce67e05d820773295e36da5a9aea2651af089b
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
      args:
      - default: 20
        help: 返回数量 (max 50)
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
      - help: 商品 ID
        name: id
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
      - help: 商品 ID
        name: id
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
      - choices:
        - default
        - sale
        - price
        default: default
        help: 排序 (default/sale销量/price价格)
        name: sort
        required: false
        type: str
      - default: 10
        help: 返回结果数量 (max 40)
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

# Taobao: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `cart` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>查看淘宝购物车 | `limit` (int, optional, default=20) |
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>淘宝商品详情 | `id` (str, required, positional) |
| `reviews` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>淘宝商品评价 | `id` (str, required, positional); `limit` (int, optional, default=10) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>淘宝商品搜索 | `query` (str, required, positional); `sort` (str, optional, default='default', choices=default,sale,price); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
