---
opencli_contract:
  version: 2
  site: jianyu
  operation: content
  policy_sha256: 72f77851b99e87f0866f5aefa86e3412e54f94075ff872a06013e36b58651cbb
  commands:
    detail:
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
      - help: Detail page URL from jianyu/search
        name: url
        positional: true
        required: true
        type: str
      - help: Optional query for evidence ranking
        name: query
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Jianyu: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `detail` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>读取剑鱼标讯详情页并抽取证据字段 | `url` (str, required, positional); `query` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
