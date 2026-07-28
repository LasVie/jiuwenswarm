---
opencli_contract:
  version: 2
  site: dongchedi
  operation: content
  policy_sha256: c6db486f5a7e9e3baa554645dbe4967de8b7363c43837b609a909d4b22065a71
  commands:
    koubei:
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
      - help: 车系 ID（来自 search 的 series_id，或 /auto/series/<id> URL）
        name: series_id
        positional: true
        required: true
        type: str
      - default: 10
        help: 返回的口碑条数（最多 15，单页 SSR 上限）
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
    models:
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
      - help: 车系 ID（来自 search 的 series_id，或 /auto/series/<id> URL）
        name: series_id
        positional: true
        required: true
        type: str
      - default: online
        help: 在售 online（默认）或停售 offline
        name: status
        required: false
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    score:
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
      - help: 车系 ID（来自 search 的 series_id，或 /auto/series/<id> URL）
        name: series_id
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    series:
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
      - help: 车系 ID（来自 search 的 series_id，或 /auto/series/<id> URL）
        name: series_id
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    specs:
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
      - help: 车系 ID（来自 search 的 series_id，或 /auto/series/<id> URL）
        name: series_id
        positional: true
        required: true
        type: str
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Dongchedi: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `koubei` | `enabled` | `public_read` / `low` | `opencli_execute(site="dongchedi", operation="content", command="koubei", arguments={"series_id":"<series_id>"})`<br>懂车帝车系口碑/车主评价（评分 / 购车款型 / 点赞 / 评论 / 正文摘要） | `series_id` (str, required, positional); `limit` (int, optional, default=10) |
| `models` | `enabled` | `public_read` / `low` | `opencli_execute(site="dongchedi", operation="content", command="models", arguments={"series_id":"<series_id>"})`<br>懂车帝车系款型列表（car_id / 名称 / 年款 / 指导价 / 经销商价 / 车主成交价） | `series_id` (str, required, positional); `status` (str, optional, default='online') |
| `score` | `enabled` | `public_read` / `low` | `opencli_execute(site="dongchedi", operation="content", command="score", arguments={"series_id":"<series_id>"})`<br>懂车帝车系评分（懂车分 8 维度 + 同级车均值对比） | `series_id` (str, required, positional) |
| `series` | `enabled` | `public_read` / `low` | `opencli_execute(site="dongchedi", operation="content", command="series", arguments={"series_id":"<series_id>"})`<br>懂车帝车系概览（品牌 / 指导价 / 二手价 / 懂车分 / 销量排名 / 在售款型数） | `series_id` (str, required, positional) |
| `specs` | `enabled` | `public_read` / `low` | `opencli_execute(site="dongchedi", operation="content", command="specs", arguments={"series_id":"<series_id>"})`<br>懂车帝车系配置概览（尺寸 / 动力 / 发动机 / 变速箱 / 四驱 / 悬挂 / 气囊） | `series_id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
