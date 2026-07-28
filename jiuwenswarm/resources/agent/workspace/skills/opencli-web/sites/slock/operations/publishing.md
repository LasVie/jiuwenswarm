---
opencli_contract:
  version: 2
  site: slock
  operation: publishing
  policy_sha256: 3b7327b298620fa16c0e1582c663796bbfffa42b1e4d50d6695d895b572bf804
  commands:
    attachment-upload:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Local file path to upload (single file; max 50 MB)
        name: file
        positional: true
        required: true
        type: str
      - help: 'channelId UUID or #name — server requires the attachment be scoped to a channel'
        name: channel
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
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
    channel-create:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Channel name
        name: name
        positional: true
        required: true
        type: str
      - help: Channel description / topic (≤500 chars)
        name: description
        required: false
        type: str
      - default: false
        help: Create a private channel instead of public
        name: private
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
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
    task-create:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
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
      - help: Task title (single; batch TODO via R4)
        name: title
        positional: true
        required: true
        type: str
      - help: Optional description body for the task
        name: desc
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
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
---

# Slock: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `attachment-upload` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Upload a local file to Slock attachments. Prints the attachmentId for use with `message-send --attach`. | `file` (str, required, positional); `channel` (str, required, positional); `server` (str, optional) |
| `channel-create` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a channel — admin only (POST /channels/). Public unless --private. | `name` (str, required, positional); `description` (str, optional); `private` (bool, optional, default=False); `server` (str, optional) |
| `task-create` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a task in a channel (single title; batch 1-50 is server-supported but client surface is single — see backlog R4). | `channel` (str, required, positional); `title` (str, required, positional); `desc` (str, optional); `server` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
