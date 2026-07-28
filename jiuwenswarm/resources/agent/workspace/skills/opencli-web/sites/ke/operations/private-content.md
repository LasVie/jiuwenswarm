---
opencli_contract:
  version: 2
  site: ke
  operation: private-content
  policy_sha256: 62f6828b3a66e65c20afcf87161d5b7a82e2e862af2c3c65325aed7bb56149df
  commands:
    chengjiao:
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
      sensitive_output:
      - private content
      - account identifiers
    ershoufang:
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
      sensitive_output:
      - private content
      - account identifiers
    xiaoqu:
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
      sensitive_output:
      - private content
      - account identifiers
    zufang:
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
      sensitive_output:
      - private content
      - account identifiers
---

# Ke: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `chengjiao` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>贝壳找房成交记录 | `city` (str, optional, default='bj'); `district` (str, optional); `limit` (int, optional, default=20) |
| `ershoufang` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>贝壳找房二手房列表 | `city` (str, optional, default='bj'); `district` (str, optional); `min-price` (int, optional); `max-price` (int, optional); `rooms` (int, optional); `limit` (int, optional, default=20) |
| `xiaoqu` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>贝壳找房小区列表 | `city` (str, optional, default='bj'); `district` (str, optional); `limit` (int, optional, default=20) |
| `zufang` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>贝壳找房租房列表 | `city` (str, optional, default='bj'); `district` (str, optional); `min-price` (int, optional); `max-price` (int, optional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
