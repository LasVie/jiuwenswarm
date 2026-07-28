---
opencli_contract:
  version: 2
  site: ctrip
  operation: private-content
  policy_sha256: 236d164805e5a6a6ff1123aad7a3fc95667019ab0cc375221cad7523b743d6cb
  commands:
    flight:
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    hotel-search:
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
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Ctrip: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `flight` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>搜索携程一程机票（按出发/到达 IATA 三字码 + 日期） | `from` (str, required, positional); `to` (str, required, positional); `date` (str, required); `limit` (int, optional, default=20) |
| `hotel-search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>搜索携程酒店列表（按城市 + 入住/离店日期） | `city` (str, required, positional); `checkin` (str, required); `checkout` (str, required); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
