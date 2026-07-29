---
opencli_contract:
  version: 2
  site: douban
  operation: content
  policy_sha256: d2fadddfa14cdb365fea4b172c4ce959c5c5179f435b303b359a5dcb000337d7
  commands:
    photos:
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
      sensitive_output: []
    subject:
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
      sensitive_output: []
---

# Douban: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `photos` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取电影海报/剧照图片列表 | `id` (str, required, positional); `type` (str, optional, default='Rb'); `limit` (int, optional, default=120) |
| `subject` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取豆瓣条目详情 | `id` (str, required, positional); `type` (str, optional, default='movie', choices=movie,book) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
