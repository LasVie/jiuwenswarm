---
opencli_contract:
  version: 2
  site: substack
  operation: discovery
  policy_sha256: 4a59cf3c0d273656b3a3677fdcbee5b42433442731ab11926b5555c4d34d5d32
  commands:
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
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="substack", operation="discovery", command="search", arguments={"keyword":"<keyword>"})`<br>搜索 Substack 文章和 Newsletter | `keyword` (str, required, positional); `type` (str, optional, default='posts', choices=posts,publications); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
