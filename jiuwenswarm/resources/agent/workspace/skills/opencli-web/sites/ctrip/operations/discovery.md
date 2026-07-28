---
opencli_contract:
  version: 2
  site: ctrip
  operation: discovery
  policy_sha256: 517de5bbe15162617396965152bf30e86782e78163f42554f80abcde4fe1acbc
  commands:
    hotel-suggest:
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
      - help: Search keyword (city, business area, or hotel name)
        name: query
        positional: true
        required: true
        type: str
      - default: 15
        help: Number of results (1-50)
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
      - help: Search keyword (city, scenic spot, landmark)
        name: query
        positional: true
        required: true
        type: str
      - default: 15
        help: Number of results (1-50)
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

# Ctrip: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `hotel-suggest` | `enabled` | `public_read` / `low` | `opencli_execute(site="ctrip", operation="discovery", command="hotel-suggest", arguments={"query":"<query>"})`<br>搜索携程酒店上下文联想：城市、商圈、单酒店匹配 | `query` (str, required, positional); `limit` (int, optional, default=15) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="ctrip", operation="discovery", command="search", arguments={"query":"<query>"})`<br>搜索携程目的地、景区、火车站和地标联想结果 | `query` (str, required, positional); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
