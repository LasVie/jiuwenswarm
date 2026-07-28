---
opencli_contract:
  version: 2
  site: douban
  operation: private-content
  policy_sha256: f2948e86776e79b572c3bb5f9dc2f05ec01adfcba950f4341f135f84b9933578
  commands:
    book-hot:
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
        help: 返回的图书数量
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
    marks:
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
      - choices:
        - collect
        - wish
        - do
        - all
        default: collect
        help: '标记类型: collect(看过), wish(想看), do(在看), all(全部)'
        name: status
        required: false
        type: str
      - default: 50
        help: 导出数量， 0 表示全部
        name: limit
        required: false
        type: int
      - help: 用户ID，不填则使用当前登录账号
        name: uid
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
    movie-hot:
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
        help: 返回的电影数量
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
    photos:
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
      - help: 电影 subject ID
        name: id
        positional: true
        required: true
        type: str
      - default: Rb
        help: 豆瓣 photos 的 type 参数，默认 Rb（海报）
        name: type
        required: false
        type: str
      - default: 120
        help: 最多返回多少张图片
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
    reviews:
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
        help: 导出数量
        name: limit
        required: false
        type: int
      - help: 用户ID，不填则使用当前登录账号
        name: uid
        required: false
        type: str
      - default: false
        help: 获取完整影评内容
        name: full
        required: false
        type: bool
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
      - choices:
        - movie
        - book
        - music
        default: movie
        help: 搜索类型（movie=电影, book=图书, music=音乐）
        name: type
        required: false
        type: str
      - help: 搜索关键词
        name: keyword
        positional: true
        required: true
        type: str
      - default: 20
        help: 返回结果数量
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
    subject:
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
      - help: 豆瓣条目 ID
        name: id
        positional: true
        required: true
        type: str
      - choices:
        - movie
        - book
        default: movie
        help: 条目类型（movie=电影, book=图书）
        name: type
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
    top250:
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
      - default: 250
        help: 返回结果数量
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

# Douban: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `book-hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>豆瓣图书热门榜单 | `limit` (int, optional, default=20) |
| `marks` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>导出个人观影标记 | `status` (str, optional, default='collect', choices=collect,wish,do,all); `limit` (int, optional, default=50); `uid` (str, optional) |
| `movie-hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>豆瓣电影热门榜单 | `limit` (int, optional, default=20) |
| `photos` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取电影海报/剧照图片列表 | `id` (str, required, positional); `type` (str, optional, default='Rb'); `limit` (int, optional, default=120) |
| `reviews` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>导出个人影评 | `limit` (int, optional, default=20); `uid` (str, optional); `full` (bool, optional, default=False) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>搜索豆瓣电影、图书或音乐 | `type` (str, optional, default='movie', choices=movie,book,music); `keyword` (str, required, positional); `limit` (int, optional, default=20) |
| `subject` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取豆瓣条目详情 | `id` (str, required, positional); `type` (str, optional, default='movie', choices=movie,book) |
| `top250` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>豆瓣电影 Top250 | `limit` (int, optional, default=250) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
