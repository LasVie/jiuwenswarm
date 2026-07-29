---
opencli_contract:
  version: 2
  site: 36kr
  operation: content
  policy_sha256: 88536c88d7c429e9f5f3cbe79917cc8453f59765a8032bb182eda43e33d93cac
  commands:
    article:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: browser_intercept
      strategy: intercept
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Article ID or full 36kr article URL
        name: id
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# 36Kr: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `article` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>获取36氪文章正文内容 | `id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
