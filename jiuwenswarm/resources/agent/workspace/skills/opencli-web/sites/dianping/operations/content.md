---
opencli_contract:
  version: 2
  site: dianping
  operation: content
  policy_sha256: d687837f891d50b475a52dc0a4ede375a721af678aeb86d2af7d141008beb6bc
  commands:
    shop:
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
      - help: 店铺 ID（来自 search 的 shop_id 列，或 https://www.dianping.com/shop/<id> URL 段）
        name: shop_id
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

# Dianping: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `shop` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>大众点评店铺详情（按 shop_id） | `shop_id` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
