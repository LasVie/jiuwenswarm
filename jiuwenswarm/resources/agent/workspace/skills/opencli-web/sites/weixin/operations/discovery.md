---
opencli_contract:
  version: 2
  site: weixin
  operation: discovery
  policy_sha256: 81c0387fc9449bde1b851ade112157695e57b200fc5cdd0c45830aae2469f9af
  commands:
    search:
      executor: browser_manifest_public_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: 搜索关键词；如需正文 Markdown，请使用 weixin download 处理公众号文章链接
        name: query
        positional: true
        required: true
        type: str
      - default: 1
        help: 结果页码，从 1 开始
        name: page
        required: false
        type: int
      - default: 10
        help: 返回条数，最大 10
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

# Weixin: discovery

Search, browse, recommend, or discover site content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `enabled` | `public_read` / `low` | `opencli_execute(site="weixin", operation="discovery", command="search", arguments={"query":"<query>"})`<br>使用搜狗微信搜索公众号文章；如需导出正文 Markdown，请使用 weixin download 处理公众号文章链接 | `query` (str, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
