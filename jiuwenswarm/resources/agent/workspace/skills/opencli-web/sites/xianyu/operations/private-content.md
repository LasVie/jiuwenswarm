---
opencli_contract:
  version: 2
  site: xianyu
  operation: private-content
  policy_sha256: 0b1f86865cbb71357073bb7e393c4e3269c06a66493a4eca1d0c53b4c0912bca
  commands:
    inbox:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: Number of conversations to return
        name: limit
        required: false
        type: int
      - default: false
        help: Return only conversations with unread messages
        name: unread-only
        required: false
        type: bool
      - default: false
        help: Click each visible conversation to resolve item_id and peer_user_id from the chat URL
        name: resolve-ids
        required: false
        type: bool
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    messages:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
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
      - default: 50
        help: Number of visible messages to return
        name: limit
        required: false
        type: int
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
      sensitive_output:
      - private content
      - account identifiers
---

# Xianyu: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `inbox` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>列出闲鱼最近私信会话 | `limit` (int, optional, default=20); `unread-only` (bool, optional, default=False); `resolve-ids` (bool, optional, default=False) |
| `messages` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>读取指定闲鱼私信会话的最近聊天内容 | `item_id` (str, optional, positional); `user_id` (str, optional, positional); `limit` (int, optional, default=50); `rank` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
