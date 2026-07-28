---
opencli_contract:
  version: 2
  site: slock
  operation: file-operations
  policy_sha256: 3b7327b298620fa16c0e1582c663796bbfffa42b1e4d50d6695d895b572bf804
  commands:
    attachment-download:
      executor: none
      execution_state: disabled
      semantic_effect: local_write
      risk: high
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
      - help: Local path to write to. Defaults to ./<attachmentId>.bin
        name: out
        required: false
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
      file_outputs:
      - workspace-relative output
      sensitive_output: []
    channel-archive:
      executor: none
      execution_state: disabled
      semantic_effect: local_write
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
      file_outputs:
      - workspace-relative output
      sensitive_output: []
---

# Slock: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `attachment-download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Download an attachment to a local file. Resolves a signed CDN URL in the page, then fetches bytes node-side (no CORS). | `attachmentId` (str, required, positional); `out` (str, optional); `server` (str, optional) |
| `channel-archive` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Archive a channel — admin only (POST /channels/:id/archive) | `channel` (str, required, positional); `server` (str, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
