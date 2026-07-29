---
opencli_contract:
  version: 2
  site: medium
  operation: discovery
  policy_sha256: ff72b54447fdc746fd7f4109325a2872a87cf9bfb1771abc1d0fd1e769ad7642
  commands:
    feed:
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
      - default: ''
        help: 话题标签（如 technology, programming, ai）
        name: topic
        required: false
        type: str
      - default: 20
        help: 返回的文章数量
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
      - help: 搜索关键词
        name: keyword
        positional: true
        required: true
        type: str
      - default: 20
        help: 返回的文章数量
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

# Medium: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `feed` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Medium 热门文章 Feed | `topic` (str, optional, default=''); `limit` (int, optional, default=20) |
| `search` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>搜索 Medium 文章 | `keyword` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
