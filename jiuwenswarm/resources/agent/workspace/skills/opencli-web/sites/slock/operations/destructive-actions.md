---
opencli_contract:
  version: 2
  site: slock
  operation: destructive-actions
  policy_sha256: e8c51aafc73ef81acbe9f554ecba65c0f2eca0cb9bc6baf4d412633ca655d97e
  commands:
    bookmark-remove:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Full messageId UUID
        name: messageId
        positional: true
        required: true
        type: str
      - help: Override active server
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    reaction-remove:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Full messageId UUID (short ids rejected)
        name: messageId
        positional: true
        required: true
        type: str
      - help: The unicode emoji to remove, e.g. 👍
        name: emoji
        positional: true
        required: true
        type: str
      - help: Override active server
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    task-delete:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Full task UUID (= message id; short ids rejected)
        name: taskId
        positional: true
        required: true
        type: str
      - default: false
        help: 'Required acknowledgement: deletion is irreversible'
        name: confirm
        required: false
        type: bool
      - help: Override active server
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    thread-unfollow:
      executor: none
      execution_state: disabled
      semantic_effect: destructive_or_admin
      risk: critical
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Thread channel UUID (from thread-list / message-read)
        name: threadChannelId
        positional: true
        required: true
        type: str
      - help: Override active server
        name: server
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

# Slock: destructive-actions

Delete, remove, revoke, or perform administrative changes.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `bookmark-remove` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Remove a bookmark (DELETE /channels/saved/:messageId). 404 is treated as already-removed. | `messageId` (str, required, positional); `server` (str, optional) |
| `reaction-remove` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Remove your emoji reaction from a message (DELETE /messages/:id/reactions). | `messageId` (str, required, positional); `emoji` (str, required, positional); `server` (str, optional) |
| `task-delete` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Delete a chat task (DELETE /tasks/:taskId). Requires --confirm — destructive, irreversible. | `taskId` (str, required, positional); `confirm` (bool, optional, default=False); `server` (str, optional) |
| `thread-unfollow` | `disabled` | `destructive_or_admin` / `critical` | Not executable; use the declared fallback if permitted<br>Stop following a thread (POST /channels/threads/unfollow) | `threadChannelId` (str, required, positional); `server` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
