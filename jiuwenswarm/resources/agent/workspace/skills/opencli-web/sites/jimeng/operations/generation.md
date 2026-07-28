---
opencli_contract:
  version: 2
  site: jimeng
  operation: generation
  policy_sha256: 15ae47373101d67908fd7e1500bdf0591d4d05f180db8b38338c6452c563cccf
  commands:
    generate:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 图片描述 prompt
        name: prompt
        positional: true
        required: true
        type: string
      - default: high_aes_general_v50
        help: '模型: high_aes_general_v50 (5.0 Lite), high_aes_general_v42 (4.6), high_aes_general_v40 (4.0)'
        name: model
        required: false
        type: string
      - default: 40
        help: 等待生成完成的秒数
        name: wait
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    new:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Jimeng: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `generate` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>即梦AI 文生图 — 输入 prompt 生成图片 | `prompt` (string, required, positional); `model` (string, optional, default='high_aes_general_v50'); `wait` (int, optional, default=40) |
| `new` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>即梦AI 新建会话（workspace） | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
