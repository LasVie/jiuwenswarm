---
opencli_contract:
  version: 2
  site: dianping
  operation: discovery
  policy_sha256: d687837f891d50b475a52dc0a4ede375a721af678aeb86d2af7d141008beb6bc
  commands:
    search:
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
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Dianping: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>大众点评店铺搜索（按关键词 + 城市） | `keyword` (str, required, positional); `city` (str, optional); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
