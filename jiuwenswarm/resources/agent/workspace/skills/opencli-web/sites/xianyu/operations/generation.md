---
opencli_contract:
  version: 2
  site: xianyu
  operation: generation
  policy_sha256: 0b1f86865cbb71357073bb7e393c4e3269c06a66493a4eca1d0c53b4c0912bca
  commands:
    chat:
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
      - help: 闲鱼商品 item_id
        name: item_id
        positional: true
        required: true
        type: str
      - help: 聊一聊对方的 user_id / peerUserId
        name: user_id
        positional: true
        required: true
        type: str
      - help: Message to send after opening the chat
        name: text
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

# Xianyu: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `chat` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>打开闲鱼聊一聊会话，并可选发送消息 | `item_id` (str, required, positional); `user_id` (str, required, positional); `text` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
