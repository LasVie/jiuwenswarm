---
opencli_contract:
  version: 2
  site: '1688'
  operation: discovery
  policy_sha256: 9b28e70491e66a1a39137448a16fa85670aedf50d50a13874cb541fef276f5a4
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# 1688: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>1688 商品搜索（结果候选、卖家链接、价格/MOQ/销量文本） | `query` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
