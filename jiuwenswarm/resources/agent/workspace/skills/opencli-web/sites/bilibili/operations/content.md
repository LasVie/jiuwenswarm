---
opencli_contract:
  version: 2
  site: bilibili
  operation: content
  policy_sha256: 6e8e73109dd43108bc96445fe5fb962e20e71bd5fabb4922fa485aa95e9accb6
  commands:
    comments:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      sensitive_output: []
    subtitle:
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
      sensitive_output: []
    summary:
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
      sensitive_output: []
    user-videos:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      sensitive_output: []
    video:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      sensitive_output: []
---

# Bilibili: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comments` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取 B站视频评论（官方 API；用 --parent <rpid> 读取某条评论下的「楼中楼」回复） | `bvid` (str, required, positional); `parent` (int, optional); `limit` (int, optional, default=20) |
| `subtitle` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取 Bilibili 视频的字幕 | `bvid` (str, required, positional); `lang` (str, optional); `page` (str, optional) |
| `summary` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取 B站视频的官方 AI 总结（视频页「AI总结」同款，含分段大纲与时间戳） | `bvid` (str, required, positional) |
| `user-videos` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>查看指定用户的投稿视频 | `uid` (str, required, positional); `limit` (int, optional, default=20); `order` (str, optional, default='pubdate'); `page` (int, optional, default=1) |
| `video` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get Bilibili video metadata (title, author, duration, stats, etc.) | `bvid` (str, required, positional); `page` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
