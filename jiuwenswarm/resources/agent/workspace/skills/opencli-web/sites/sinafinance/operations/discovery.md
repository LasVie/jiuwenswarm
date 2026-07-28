---
opencli_contract:
  version: 2
  site: sinafinance
  operation: discovery
  policy_sha256: 1deddb0b1999a7b26b75c49f000c61dc7a75a8dc92dc700605ccb6dedcf9a8c7
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
---

# Sinafinance: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `news` | `enabled` | `public_read` / `low` | `opencli_execute(site="sinafinance", operation="discovery", command="news")`<br>新浪财经 7x24 小时实时快讯 | `limit` (int, optional, default=20); `type` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
