---
opencli_contract:
  version: 2
  site: ke
  operation: discovery
  policy_sha256: 1667e3db1a02c799f2785c49de06bafdb24c882201228860fae6eb5d8326c56a
  commands:
    chengjiao:
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
      - default: bj
        help: 城市代码，如 bj(北京), sh(上海), gz(广州), sz(深圳), zs(中山)
        name: city
        required: false
        type: str
      - help: 区域拼音，如 chaoyang, haidian
        name: district
        required: false
        type: str
      - default: 20
        help: 返回数量
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    ershoufang:
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
      - default: bj
        help: 城市代码，如 bj(北京), sh(上海), gz(广州), sz(深圳), zs(中山)
        name: city
        required: false
        type: str
      - help: 区域拼音，如 chaoyang, haidian, tianhe
        name: district
        required: false
        type: str
      - help: 最低总价（万元）
        name: min-price
        required: false
        type: int
      - help: 最高总价（万元）
        name: max-price
        required: false
        type: int
      - help: 几居室 (1-5)
        name: rooms
        required: false
        type: int
      - default: 20
        help: 返回数量
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    xiaoqu:
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
      - default: bj
        help: 城市代码，如 bj(北京), sh(上海), gz(广州), sz(深圳), zs(中山)
        name: city
        required: false
        type: str
      - help: 区域拼音，如 chaoyang, haidian
        name: district
        required: false
        type: str
      - default: 20
        help: 返回数量
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    zufang:
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
      - default: bj
        help: 城市代码，如 bj(北京), sh(上海), gz(广州), sz(深圳), zs(中山)
        name: city
        required: false
        type: str
      - help: 区域拼音，如 chaoyang, haidian
        name: district
        required: false
        type: str
      - help: 最低月租（元）
        name: min-price
        required: false
        type: int
      - help: 最高月租（元）
        name: max-price
        required: false
        type: int
      - default: 20
        help: 返回数量
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Ke: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `chengjiao` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>贝壳找房成交记录 | `city` (str, optional, default='bj'); `district` (str, optional); `limit` (int, optional, default=20) |
| `ershoufang` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>贝壳找房二手房列表 | `city` (str, optional, default='bj'); `district` (str, optional); `min-price` (int, optional); `max-price` (int, optional); `rooms` (int, optional); `limit` (int, optional, default=20) |
| `xiaoqu` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>贝壳找房小区列表 | `city` (str, optional, default='bj'); `district` (str, optional); `limit` (int, optional, default=20) |
| `zufang` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>贝壳找房租房列表 | `city` (str, optional, default='bj'); `district` (str, optional); `min-price` (int, optional); `max-price` (int, optional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
