---
opencli_contract:
  version: 2
  site: 36kr
  operation: discovery
  policy_sha256: 88536c88d7c429e9f5f3cbe79917cc8453f59765a8032bb182eda43e33d93cac
  commands:
    hot:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Number of items (max 50)
        name: limit
        required: false
        type: int
      - default: catalog
        help: 'List type: renqi (人气), zonghe (综合), shoucang (收藏), catalog (热门资讯)'
        name: type
        required: false
        type: string
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
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
        help: Number of articles (max 50)
        name: limit
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    search:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Search keyword (e.g. "AI", "OpenAI")
        name: query
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of results (max 50)
        name: limit
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

# 36Kr: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hot` | `enabled` | `public_read` / `low` | `opencli_execute(site="36kr", operation="discovery", command="hot")`<br>36氪热榜 — trending articles (renqi/zonghe/shoucang/catalog) | `limit` (int, optional, default=20); `type` (string, optional, default='catalog') |
| `news` | `enabled` | `public_read` / `low` | `opencli_execute(site="36kr", operation="discovery", command="news")`<br>Latest tech/startup news from 36kr (36氪) | `limit` (int, optional, default=20) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="36kr", operation="discovery", command="search", arguments={"query":"<query>"})`<br>搜索36氪文章 | `query` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
