---
opencli_contract:
  version: 2
  site: dianping
  operation: private-content
  policy_sha256: 800ec45fdb7edd853be622ec4773c40c01738a5eca4c5893a35cfaef559f5193
  commands:
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
      - help: 搜索关键词，例如 "火锅"
        name: keyword
        positional: true
        required: true
        type: str
      - help: 城市名（北京/上海/汕头/beijing/shantou/...）或 cityId 数字。未在静态表中的城市会通过 dianping.com 在线解析。不传则使用 cookie 默认城市
        name: city
        required: false
        type: str
      - default: 15
        help: 返回的店铺数量（最多 15，dianping 单页固定 15 条）
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
    shop:
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
      - help: 店铺 ID（来自 search 的 shop_id 列，或 https://www.dianping.com/shop/<id> URL 段）
        name: shop_id
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

# Dianping: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>大众点评店铺搜索（按关键词 + 城市） | `keyword` (str, required, positional); `city` (str, optional); `limit` (int, optional, default=15) |
| `shop` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>大众点评店铺详情（按 shop_id） | `shop_id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
