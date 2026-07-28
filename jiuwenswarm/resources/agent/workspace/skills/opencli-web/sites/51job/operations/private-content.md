---
opencli_contract:
  version: 2
  site: 51job
  operation: private-content
  policy_sha256: 9bdaf7dad3b5f51e7aa74b0a4953fda4b5c23a887a2df94d495976962b32989c
  commands:
    company:
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
      - help: 加密公司 ID（search 返回的 encCoId）
        name: encCoId
        positional: true
        required: true
        type: string
      - default: 20
        help: 返回职位数（1-50）
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
    detail:
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
      - help: 职位 ID（search 返回的 jobId）
        name: jobId
        positional: true
        required: true
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    hot:
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
      - default: 全国
        help: 城市名或 6 位城市码（默认 "全国"）
        name: area
        required: false
        type: string
      - default: 综合
        help: 排序：综合 / 最新 / 薪资 / 距离
        name: sort
        required: false
        type: string
      - default: 1
        help: 页码（1-based）
        name: page
        required: false
        type: int
      - default: 20
        help: 返回条数（1-50）
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
    search:
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
      - help: 搜索关键词（岗位名 / 技能 / 公司）
        name: keyword
        positional: true
        required: true
        type: string
      - default: 全国
        help: 城市名或 6 位城市码（如 "杭州" / "080200" / "全国"）
        name: area
        required: false
        type: string
      - default: ''
        help: 薪资区间（如 "10-15k" / "1-1.5万" / "20-30k"）
        name: salary
        required: false
        type: string
      - default: ''
        help: 工作年限（如 "应届" / "1-3年" / "3-5年" / "5-7年"）
        name: experience
        required: false
        type: string
      - default: ''
        help: 学历要求（如 "本科" / "大专" / "硕士"）
        name: degree
        required: false
        type: string
      - default: ''
        help: 公司性质（如 "外资" / "国企" / "民营"）
        name: companyType
        required: false
        type: string
      - default: ''
        help: 公司规模（如 "50-150" / "1000-5000"）
        name: companySize
        required: false
        type: string
      - default: 综合
        help: 排序：综合 / 最新 / 薪资 / 距离
        name: sort
        required: false
        type: string
      - default: 1
        help: 页码（1-based）
        name: page
        required: false
        type: int
      - default: 20
        help: 返回条数（1-50）
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

# 51Job: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `company` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>51job 公司简介 + 在招职位（按 encCoId） | `encCoId` (string, required, positional); `limit` (int, optional, default=20) |
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>51job 职位详情（按 jobId） | `jobId` (string, required, positional) |
| `hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>51job 推荐职位（按城市/行业/排序浏览） | `area` (string, optional, default='全国'); `sort` (string, optional, default='综合'); `page` (int, optional, default=1); `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>51job 前程无忧关键词职位搜索 | `keyword` (string, required, positional); `area` (string, optional, default='全国'); `salary` (string, optional, default=''); `experience` (string, optional, default=''); `degree` (string, optional, default=''); `companyType` (string, optional, default=''); `companySize` (string, optional, default=''); `sort` (string, optional, default='综合'); `page` (int, optional, default=1); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
