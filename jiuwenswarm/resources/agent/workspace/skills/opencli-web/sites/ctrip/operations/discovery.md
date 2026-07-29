---
opencli_contract:
  version: 2
  site: ctrip
  operation: discovery
  policy_sha256: 3349d00749ad278cd9d82659b69987a2557778a84a1a4d279377382e2458511a
  commands:
    flight:
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
      - help: Departure IATA code (e.g. BJS / PEK)
        name: from
        positional: true
        required: true
        type: str
      - help: Arrival IATA code (e.g. SHA / PVG)
        name: to
        positional: true
        required: true
        type: str
      - help: Departure date (YYYY-MM-DD)
        name: date
        required: true
        type: str
      - default: 20
        help: Number of flights (1-50)
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
    hotel-search:
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
      - help: Numeric Ctrip city ID (use `ctrip search` or `ctrip hotel-suggest` to discover)
        name: city
        positional: true
        required: true
        type: str
      - help: Check-in date (YYYY-MM-DD)
        name: checkin
        required: true
        type: str
      - help: Check-out date (YYYY-MM-DD)
        name: checkout
        required: true
        type: str
      - default: 10
        help: Number of hotels (1-30); SSR first page returns ~13 entries
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
| `flight` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>搜索携程一程机票（按出发/到达 IATA 三字码 + 日期） | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (int, optional, default=20) |
| `hotel-search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>搜索携程酒店列表（按城市 + 入住/离店日期） | `city` (str, required, positional); `checkin` (str, required); `checkout` (str, required); `limit` (int, optional, default=10) |
| `hotel-suggest` | `enabled` | `public_read` / `low` | `opencli_execute(site="ctrip", operation="discovery", command="hotel-suggest", arguments={"query":"<query>"})`<br>搜索携程酒店上下文联想：城市、商圈、单酒店匹配 | `query` (str, required, positional); `limit` (int, optional, default=15) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="ctrip", operation="discovery", command="search", arguments={"query":"<query>"})`<br>搜索携程目的地、景区、火车站和地标联想结果 | `query` (str, required, positional); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
