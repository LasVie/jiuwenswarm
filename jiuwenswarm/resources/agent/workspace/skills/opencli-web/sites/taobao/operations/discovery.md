---
opencli_contract:
  version: 2
  site: taobao
  operation: discovery
  policy_sha256: ccad1ba7122a7b2e2c47319457d544a57c6b1bcfc5e1c9e981289915d375741f
  commands:
    search:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Taobao: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>淘宝商品搜索 | `query` (str, required, positional); `sort` (str, optional, default='default', choices=default,sale,price); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
