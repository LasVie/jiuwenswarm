---
opencli_contract:
  version: 2
  site: '1688'
  operation: content
  policy_sha256: 9b28e70491e66a1a39137448a16fa85670aedf50d50a13874cb541fef276f5a4
  commands:
    assets:
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
      - help: 1688 商品 URL 或 offer ID（如 887904326744）
        name: input
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
    item:
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
      - help: 1688 商品 URL 或 offer ID（如 887904326744）
        name: input
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
    store:
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
      - help: 1688 店铺 URL 或 member ID（如 b2b-22154705262941f196）
        name: input
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

# 1688: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `assets` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>列出 1688 商品页可提取的图片/视频素材 | `input` (str, required, positional) |
| `item` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>1688 商品详情（公开商品字段、价格阶梯、卖家基础信息） | `input` (str, required, positional) |
| `store` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>1688 店铺/供应商公开信息（联系方式、主营、入驻年限、公开服务信号） | `input` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
