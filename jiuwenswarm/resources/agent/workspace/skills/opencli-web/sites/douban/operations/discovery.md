---
opencli_contract:
  version: 2
  site: douban
  operation: discovery
  policy_sha256: d2fadddfa14cdb365fea4b172c4ce959c5c5179f435b303b359a5dcb000337d7
  commands:
    book-hot:
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
      sensitive_output: []
    movie-hot:
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
      sensitive_output: []
    search:
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
      sensitive_output: []
    top250:
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
      sensitive_output: []
---

# Douban: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `book-hot` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>豆瓣图书热门榜单 | `limit` (int, optional, default=20) |
| `movie-hot` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>豆瓣电影热门榜单 | `limit` (int, optional, default=20) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>搜索豆瓣电影、图书或音乐 | `type` (str, optional, default='movie', choices=movie,book,music); `keyword` (str, required, positional); `limit` (int, optional, default=20) |
| `top250` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>豆瓣电影 Top250 | `limit` (int, optional, default=250) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
