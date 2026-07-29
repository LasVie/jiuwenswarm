---
opencli_contract:
  version: 2
  site: sinafinance
  operation: discovery
  policy_sha256: 4da364824284b2a791afdae01ce7b10e3add231b1296676d121f44fa916ab7fc
  commands:
    news:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Max results (max 50)
        name: limit
        required: false
        type: int
      - default: 0
        help: 'News type: 0=全部 1=A股 2=宏观 3=公司 4=数据 5=市场 6=国际 7=观点 8=央行 9=其它'
        name: type
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    rolling-news:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    stock-rank:
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
      - choices:
        - cn
        - hk
        - us
        - wh
        - ft
        default: cn
        help: 'Market: cn (A股), hk (港股), us (美股), wh (外汇), ft (期货)'
        name: market
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Sinafinance: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `news` | `enabled` | `public_read` / `low` | `opencli_execute(site="sinafinance", operation="discovery", command="news")`<br>新浪财经 7x24 小时实时快讯 | `limit` (int, optional, default=20); `type` (int, optional, default=0) |
| `rolling-news` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>新浪财经滚动新闻 | none |
| `stock-rank` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>新浪财经热搜榜 | `market` (string, optional, default='cn', choices=cn,hk,us,wh,ft) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
