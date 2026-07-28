---
opencli_contract:
  version: 2
  site: bilibili
  operation: private-content
  policy_sha256: 79262d9ab33f66ec264abde1f4e74f443b2285e92443fd0272d5197bfc948436
  commands:
    comments:
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
      - help: Video BV ID (e.g. BV1WtAGzYEBm)
        name: bvid
        positional: true
        required: true
        type: str
      - help: rpid of a comment — fetch the replies under it instead of top-level comments
        name: parent
        required: false
        type: int
      - default: 20
        help: Number of comments (max 50)
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
    dynamic:
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
      - default: 15
        help: ''
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
    feed:
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
      - help: 用户 UID 或用户名（不传则显示关注时间线）
        name: uid
        positional: true
        required: false
        type: str
      - default: 20
        help: Max results to return
        name: limit
        required: false
        type: int
      - default: all
        help: 'Filter: all, video, article, draw, text'
        name: type
        required: false
        type: str
      - default: 1
        help: Number of pages to fetch (each ~20 items)
        name: pages
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
    feed-detail:
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
      - help: 动态 ID（从 feed 命令的 url 中获取）
        name: id
        positional: true
        required: true
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
    following:
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
      - help: 目标用户 ID（默认为当前登录用户）
        name: uid
        positional: true
        required: false
        type: str
      - default: 1
        help: 页码
        name: page
        required: false
        type: int
      - default: 50
        help: 每页数量 (最大 50)
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
    history:
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
        help: Number of results
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
      - default: 20
        help: Number of videos
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
    ranking:
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
        help: ''
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
      - help: Search keyword
        name: query
        positional: true
        required: true
        type: str
      - default: video
        help: video or user
        name: type
        required: false
        type: str
      - default: 1
        help: Result page
        name: page
        required: false
        type: int
      - default: 20
        help: Number of results
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
    subtitle:
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
      - help: Bilibili 视频 BV ID（如 BV1xx411c7mD），或视频 URL / b23.tv 短链
        name: bvid
        positional: true
        required: true
        type: str
      - help: 字幕语言代码 (如 zh-CN, en-US, ai-zh)，默认取第一个
        name: lang
        required: false
        type: str
      - help: 分P 选集序号（从 1 开始）。多 P 视频取该集字幕；缺省取默认 P1
        name: page
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
    summary:
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
      - help: Video BV ID / URL / b23.tv short link
        name: bvid
        positional: true
        required: true
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
    user-videos:
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
      - help: User UID or username
        name: uid
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of results
        name: limit
        required: false
        type: int
      - default: pubdate
        help: 'Sort: pubdate, click, stow'
        name: order
        required: false
        type: str
      - default: 1
        help: Page number
        name: page
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
    video:
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
      - help: BV ID, video URL, or b23.tv short link
        name: bvid
        positional: true
        required: true
        type: str
      - help: 分P 选集序号（从 1 开始）。多 P 视频指定某一集，title/cid 返回该集；缺省取整集默认（P1）
        name: page
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

# Bilibili: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comments` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取 B站视频评论（官方 API；用 --parent <rpid> 读取某条评论下的「楼中楼」回复） | `bvid` (str, required, positional); `parent` (int, optional); `limit` (int, optional, default=20) |
| `dynamic` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get Bilibili user dynamic feed | `limit` (int, optional, default=15) |
| `feed` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>动态时间线（不传 uid 查关注时间线，传 uid 查指定用户动态） | `uid` (str, optional, positional); `limit` (int, optional, default=20); `type` (str, optional, default='all'); `pages` (int, optional, default=1) |
| `feed-detail` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>查看 Bilibili 动态详情（支持充电专属内容） | `id` (str, required, positional) |
| `following` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取 Bilibili 用户的关注列表 | `uid` (str, optional, positional); `page` (int, optional, default=1); `limit` (int, optional, default=50) |
| `history` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>我的观看历史 | `limit` (int, optional, default=20) |
| `hot` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>B站热门视频 | `limit` (int, optional, default=20) |
| `ranking` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get Bilibili video ranking board | `limit` (int, optional, default=20) |
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search Bilibili videos or users | `query` (str, required, positional); `type` (str, optional, default='video'); `page` (int, optional, default=1); `limit` (int, optional, default=20) |
| `subtitle` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取 Bilibili 视频的字幕 | `bvid` (str, required, positional); `lang` (str, optional); `page` (str, optional) |
| `summary` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>获取 B站视频的官方 AI 总结（视频页「AI总结」同款，含分段大纲与时间戳） | `bvid` (str, required, positional) |
| `user-videos` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>查看指定用户的投稿视频 | `uid` (str, required, positional); `limit` (int, optional, default=20); `order` (str, optional, default='pubdate'); `page` (int, optional, default=1) |
| `video` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get Bilibili video metadata (title, author, duration, stats, etc.) | `bvid` (str, required, positional); `page` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
