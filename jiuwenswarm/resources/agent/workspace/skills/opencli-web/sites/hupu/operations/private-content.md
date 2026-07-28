---
opencli_contract:
  version: 2
  site: hupu
  operation: private-content
  policy_sha256: 292f24b86db7d4f26303e6f4a06f0f3d1645ab8dd5f083536c37d5c5d2acee73
  commands:
    detail:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 帖子ID（9位数字）
        name: tid
        positional: true
        required: true
        type: str
      - default: false
        help: 是否包含热门回复
        name: replies
        required: false
        type: boolean
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
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Number of threads (1-100)
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
    mentions:
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
      - default: 20
        help: 最多返回多少条消息
        name: limit
        required: false
        type: int
      - default: 3
        help: 最多抓取多少页
        name: max_pages
        required: false
        type: int
      - help: 分页游标；不传时从第一页开始
        name: page_str
        required: false
        type: str
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
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 搜索关键词
        name: query
        positional: true
        required: true
        type: str
      - default: 1
        help: 结果页码
        name: page
        required: false
        type: int
      - default: 20
        help: 返回结果数量
        name: limit
        required: false
        type: int
      - help: 板块ID过滤 (可选)
        name: forum
        required: false
        type: str
      - default: general
        help: '排序方式: general/createtime/replytime/light/reply'
        name: sort
        required: false
        type: str
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

# Hupu: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取虎扑帖子详情 (使用Next.js JSON数据) | `tid` (str, required, positional); `replies` (boolean, optional, default=False) |
| `hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>虎扑首页热门帖子（含 lights / replies / forum / is_hot 列） | `limit` (int, optional, default=20) |
| `mentions` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>查看虎扑提到我的回复 (需要登录) | `limit` (int, optional, default=20); `max_pages` (int, optional, default=3); `page_str` (str, optional) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>搜索虎扑帖子 (使用官方API) | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=20); `forum` (str, optional); `sort` (str, optional, default='general') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
