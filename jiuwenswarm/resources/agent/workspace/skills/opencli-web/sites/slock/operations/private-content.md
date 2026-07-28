---
opencli_contract:
  version: 2
  site: slock
  operation: private-content
  policy_sha256: 3b7327b298620fa16c0e1582c663796bbfffa42b1e4d50d6695d895b572bf804
  commands:
    attachment-url:
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
      - help: Attachment UUID
        name: attachmentId
        positional: true
        required: true
        type: str
      - help: Override active server slug
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    bookmark-list:
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
      - default: 50
        help: Max results
        name: limit
        required: false
        type: int
      - default: 0
        help: Offset
        name: offset
        required: false
        type: int
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
      sensitive_output:
      - private content
      - account identifiers
    channel-files:
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
      - help: 'channelId UUID or #name'
        name: channel
        positional: true
        required: true
        type: str
      - default: 50
        help: Max files
        name: limit
        required: false
        type: int
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
      sensitive_output:
      - private content
      - account identifiers
    channel-info:
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
      sensitive_output:
      - private content
      - account identifiers
    channel-list:
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
      - help: Override active server (slug or id) for this call
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    channel-members:
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
      - help: 'channelId UUID or #name'
        name: channel
        positional: true
        required: true
        type: str
      - help: Override active server (slug or id)
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    dm-list:
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
      - help: Override active server (slug or id)
        name: server
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
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
      - default: all
        help: all | unread | mentions
        name: filter
        required: false
        type: str
      - default: 30
        help: Max items (server caps at 100)
        name: limit
        required: false
        type: int
      - default: 0
        help: Pagination offset
        name: offset
        required: false
        type: int
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
      sensitive_output:
      - private content
      - account identifiers
    message-read:
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
      - help: channelId UUID, "#name", or "#channel:msgIdOrShort"
        name: channel
        positional: true
        required: true
        type: str
      - help: 'Cursor: seq number or messageId UUID (exclusive)'
        name: after
        required: false
        type: str
      - help: seq to page before
        name: before
        required: false
        type: str
      - default: 50
        help: Max messages
        name: limit
        required: false
        type: int
      - default: false
        help: Skip /threads enrichment
        name: no-threads
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
      sensitive_output:
      - private content
      - account identifiers
    message-search:
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
      - help: Search query
        name: query
        positional: true
        required: true
        type: str
      - help: 'Restrict to a channel (UUID or #name)'
        name: channel
        required: false
        type: str
      - default: 50
        help: Max results
        name: limit
        required: false
        type: int
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
      sensitive_output:
      - private content
      - account identifiers
    server-list:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    task-get:
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
      - help: 'channelId UUID or #name'
        name: channel
        positional: true
        required: true
        type: str
      - help: 'taskNumber (per-channel integer, as shown in "task #N")'
        name: number
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
      sensitive_output:
      - private content
      - account identifiers
    task-list:
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
      - help: 'channelId UUID or #name'
        name: channel
        positional: true
        required: true
        type: str
      - help: 'Filter by status: todo|in_progress|in_review|done|closed'
        name: status
        required: false
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
      sensitive_output:
      - private content
      - account identifiers
    task-list-server:
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
      - help: 'Filter by status: todo|in_progress|in_review|done|closed'
        name: status
        required: false
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
      sensitive_output:
      - private content
      - account identifiers
    thread-list:
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
      sensitive_output:
      - private content
      - account identifiers
    unread-summary:
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
      args: []
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

# Slock: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `attachment-url` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get a short-lived signed CDN URL for an attachment (does not download bytes). | `attachmentId` (str, required, positional); `server` (str, optional) |
| `bookmark-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List bookmarks (saved messages) in the active server | `limit` (int, optional, default=50); `offset` (int, optional, default=0); `server` (str, optional) |
| `channel-files` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List files shared in a channel (GET /channels/:id/files) | `channel` (str, required, positional); `limit` (int, optional, default=50); `server` (str, optional) |
| `channel-info` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show one channel's details (GET /channels/:id) | `channel` (str, required, positional); `server` (str, optional) |
| `channel-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List channels in the active slock server | `server` (str, optional) |
| `channel-members` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List members of a channel | `channel` (str, required, positional); `server` (str, optional) |
| `dm-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List DM channels in the active server (GET /channels/dm) | `server` (str, optional) |
| `inbox` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List unified inbox items (channels, DMs, followed threads) that need attention. | `filter` (str, optional, default='all'); `limit` (int, optional, default=30); `offset` (int, optional, default=0); `server` (str, optional) |
| `message-read` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Read messages in a channel or thread. Thread form: "#channel:msgIdOrShort". Use --after seq\|UUID for cursor. | `channel` (str, required, positional); `after` (str, optional); `before` (str, optional); `limit` (int, optional, default=50); `no-threads` (bool, optional, default=False); `server` (str, optional) |
| `message-search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search messages | `query` (str, required, positional); `channel` (str, optional); `limit` (int, optional, default=50); `server` (str, optional) |
| `server-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List slock servers you belong to; marks active per localStorage slug | none |
| `task-get` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Fetch a task by channel + taskNumber (GET /tasks/channel/:channelId/number/:taskNumber). | `channel` (str, required, positional); `number` (str, required, positional); `server` (str, optional) |
| `task-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List tasks (chat tasks = messages with task fields) attached to a channel. Optional --status filter. | `channel` (str, required, positional); `status` (str, optional); `server` (str, optional) |
| `task-list-server` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List tasks across all channels in the active server (GET /tasks/server). Optional --status filter. | `status` (str, optional); `server` (str, optional) |
| `thread-list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List followed threads in the active server (GET /channels/threads/followed) | `server` (str, optional) |
| `unread-summary` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Global unread counts across every server you belong to. | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
