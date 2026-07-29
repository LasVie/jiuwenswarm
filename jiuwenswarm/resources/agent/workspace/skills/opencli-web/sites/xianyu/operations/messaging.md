---
opencli_contract:
  version: 2
  site: xianyu
  operation: messaging
  policy_sha256: 0b1f86865cbb71357073bb7e393c4e3269c06a66493a4eca1d0c53b4c0912bca
  commands:
    reply:
      executor: none
      execution_state: disabled
      semantic_effect: message_send
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
        required: false
        type: str
      - help: 聊一聊对方的 user_id / peerUserId
        name: user_id
        positional: true
        required: false
        type: str
      - help: Message text to send
        name: text
        required: true
        type: str
      - default: 0
        help: Conversation rank from xianyu inbox; clicks the visible row instead of requiring IDs
        name: rank
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

# Xianyu: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `reply` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>回复指定闲鱼私信会话 | `item_id` (str, optional, positional); `user_id` (str, optional, positional); `text` (str, required); `rank` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
