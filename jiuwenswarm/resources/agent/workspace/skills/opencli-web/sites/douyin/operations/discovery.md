---
opencli_contract:
  version: 2
  site: douyin
  operation: discovery
  policy_sha256: 44a88f4e2945603337450f4d82e1d94d30556064265afb43719f582edd8ebf4c
  commands:
    location:
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
      - help: 地名关键词
        name: query
        positional: true
        required: true
        type: str
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
      sensitive_output: []
    search:
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
      - help: 搜索关键词
        name: query
        positional: true
        required: true
        type: str
      - default: 10
        help: 结果数量 (1-30)
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
    user-videos:
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
      - help: 用户 sec_uid（URL 末尾部分）
        name: sec_uid
        positional: true
        required: true
        type: string
      - default: 20
        help: 获取数量（最大 20）
        name: limit
        required: false
        type: int
      - default: true
        help: '包含热门评论（默认: true）'
        name: with_comments
        required: false
        type: bool
      - default: 10
        help: 每个视频获取多少条评论（最大 10）
        name: comment_limit
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

# Douyin: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `location` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>地理位置 POI 搜索 | `query` (str, required, positional); `limit` (int, optional, default=20) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>关键词搜索抖音视频 | `query` (str, required, positional); `limit` (int, optional, default=10) |
| `user-videos` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取指定用户的视频列表（含下载地址和热门评论） | `sec_uid` (string, required, positional); `limit` (int, optional, default=20); `with_comments` (bool, optional, default=True); `comment_limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
