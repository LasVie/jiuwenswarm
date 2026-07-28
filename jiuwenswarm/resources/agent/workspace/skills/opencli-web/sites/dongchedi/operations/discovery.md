---
opencli_contract:
  version: 2
  site: dongchedi
  operation: discovery
  policy_sha256: c6db486f5a7e9e3baa554645dbe4967de8b7363c43837b609a909d4b22065a71
  commands:
    search:
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
      - help: 搜索关键词，例如 "宝马X5" 或 "汉兰达"
        name: keyword
        positional: true
        required: true
        type: str
      - default: 15
        help: 返回的车系数量（最多 30）
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

# Dongchedi: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="dongchedi", operation="discovery", command="search", arguments={"keyword":"<keyword>"})`<br>懂车帝车系搜索（按关键词，返回车系 + 指导价/经销商价） | `keyword` (str, required, positional); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
