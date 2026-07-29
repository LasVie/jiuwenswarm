---
opencli_contract:
  version: 2
  site: bilibili
  operation: messaging
  policy_sha256: 6e8e73109dd43108bc96445fe5fb962e20e71bd5fabb4922fa485aa95e9accb6
  commands:
    comment:
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
      - help: Video BV ID / URL / b23.tv short link
        name: bvid
        positional: true
        required: true
        type: str
      - help: Comment text. Any @username in it is resolved to a real mention
        name: message
        positional: true
        required: true
        type: str
      - help: top-level/root rpid to reply under (omit for a top-level comment)
        name: parent
        required: false
        type: int
      - help: Actually post the comment. Without it the command refuses to write.
        name: execute
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Bilibili: messaging

Send messages, replies, comments, invitations, or contacts.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comment` | `disabled` | `message_send` / `high` | Not executable; use the declared fallback if permitted<br>在 B站视频下发表评论或回复（官方 API，需登录；消息里的 @用户 会被解析为真实提及） | `bvid` (str, required, positional); `message` (str, required, positional); `parent` (int, optional); `execute` (boolean, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
