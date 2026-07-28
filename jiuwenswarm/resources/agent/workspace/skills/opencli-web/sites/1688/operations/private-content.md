---
opencli_contract:
  version: 2
  site: '1688'
  operation: private-content
  policy_sha256: 95bb385d5569ba5b9635a4f8ae6128daa6445314073f4bb352b00ef7932a0423
  commands:
    assets:
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
      - help: 1688 商品 URL 或 offer ID（如 887904326744）
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
      - help: 1688 商品 URL 或 offer ID（如 887904326744）
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
      - help: 搜索关键词，如 "置物架"
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: 结果数量上限（默认 20，最大 100）
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
    store:
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
      - help: 1688 店铺 URL 或 member ID（如 b2b-22154705262941f196）
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
---

# 1688: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `assets` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>列出 1688 商品页可提取的图片/视频素材 | `input` (str, required, positional) |
| `item` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>1688 商品详情（公开商品字段、价格阶梯、卖家基础信息） | `input` (str, required, positional) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>1688 商品搜索（结果候选、卖家链接、价格/MOQ/销量文本） | `query` (str, required, positional); `limit` (int, optional, default=20) |
| `store` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>1688 店铺/供应商公开信息（联系方式、主营、入驻年限、公开服务信号） | `input` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
