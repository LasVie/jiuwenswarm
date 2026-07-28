---
opencli_contract:
  version: 2
  site: slock
  operation: write-actions
  policy_sha256: 3b7327b298620fa16c0e1582c663796bbfffa42b1e4d50d6695d895b572bf804
  commands:
    channel-join:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 'channelId UUID or #name'
        name: channel
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
    channel-leave:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 'channelId UUID or #name'
        name: channel
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
    channel-mark:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 'channelId UUID or #name'
        name: channel
        positional: true
        required: true
        type: str
      - help: Mark read up to this seq (omit for read-all)
        name: seq
        required: false
        type: int
      - default: false
        help: Mark the channel unread instead of read
        name: unread
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
    channel-unarchive:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 'channelId UUID or #name'
        name: channel
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
    inbox-done:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: 'channelId UUID or #name'
        name: channel
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
    inbox-read-all:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
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
    reaction-add:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
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
      - help: A single unicode emoji, e.g. 👍
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
    server-use:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: server slug, "#slug", or UUID id
        name: input
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    task-claim:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
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
    task-convert:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Full message UUID, or "#channel:shortId" (short id expanded via /messages/context)
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
    task-status:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
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
      - help: 'One of: todo|in_progress|in_review|done|closed'
        name: status
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
    task-unclaim:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
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
    thread-done:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
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
    thread-undone:
      executor: none
      execution_state: disabled
      semantic_effect: reversible_remote_write
      risk: high
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

# Slock: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `channel-join` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Join a public channel (POST /channels/:id/join) | `channel` (str, required, positional); `server` (str, optional) |
| `channel-leave` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Leave a channel (POST /channels/:id/leave) | `channel` (str, required, positional); `server` (str, optional) |
| `channel-mark` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Mark a channel read (default), read up to --seq, or --unread. | `channel` (str, required, positional); `seq` (int, optional); `unread` (bool, optional, default=False); `server` (str, optional) |
| `channel-unarchive` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Unarchive a channel — admin only (POST /channels/:id/unarchive). #name lookups exclude archived channels; pass the channelId UUID for archived ones. | `channel` (str, required, positional); `server` (str, optional) |
| `inbox-done` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Mark one chat as done / clear it from the inbox (POST /channels/inbox/done) | `channel` (str, required, positional); `server` (str, optional) |
| `inbox-read-all` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Mark the entire inbox as read (POST /channels/inbox/read-all) | `server` (str, optional) |
| `reaction-add` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Add an emoji reaction to a message (POST /messages/:id/reactions). Idempotent server-side. | `messageId` (str, required, positional); `emoji` (str, required, positional); `server` (str, optional) |
| `server-use` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Set the active slock server (writes localStorage.slock_last_server_slug) | `input` (str, required, positional) |
| `task-claim` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Claim a chat task (PATCH /tasks/:id/claim). Requires full task UUID (= message id). | `taskId` (str, required, positional); `server` (str, optional) |
| `task-convert` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Convert a message into a chat task (POST /tasks/convert-message). Accepts a message UUID or "#channel:shortId". | `messageId` (str, required, positional); `server` (str, optional) |
| `task-status` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Set a task's status (PATCH /tasks/:taskId/status, body {status}). One of todo\|in_progress\|in_review\|done\|closed. | `taskId` (str, required, positional); `status` (str, required, positional); `server` (str, optional) |
| `task-unclaim` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Release ownership of a chat task (PATCH /tasks/:id/unclaim). | `taskId` (str, required, positional); `server` (str, optional) |
| `thread-done` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Mark a thread as done / hide it from the active list (POST /channels/threads/done) | `threadChannelId` (str, required, positional); `server` (str, optional) |
| `thread-undone` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Restore a done thread to the active list (POST /channels/threads/undone) | `threadChannelId` (str, required, positional); `server` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
