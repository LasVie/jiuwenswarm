---
opencli_contract:
  version: 2
  site: substack
  operation: discovery
  policy_sha256: df8ef4f8daaf608fb76501375020aa60d8556a54b751921df910bcbdd175773f
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
      - default: all
        help: '文章分类: all, tech, business, culture, politics, science, health'
        name: category
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
      - help: 搜索关键词
        name: keyword
        positional: true
        required: true
        type: str
      - choices:
        - posts
        - publications
        default: posts
        help: 搜索类型（posts=文章, publications=Newsletter）
        name: type
        required: false
        type: str
      - default: 20
        help: 返回结果数量
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
---

# Substack: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `feed` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Substack 热门文章 Feed | `category` (str, optional, default='all'); `limit` (int, optional, default=20) |
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="substack", operation="discovery", command="search", arguments={"keyword":"<keyword>"})`<br>搜索 Substack 文章和 Newsletter | `keyword` (str, required, positional); `type` (str, optional, default='posts', choices=posts,publications); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
