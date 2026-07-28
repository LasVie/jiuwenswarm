---
opencli_contract:
  version: 2
  site: grok
  operation: file-operations
  policy_sha256: d2b9f216523df47c74346d35cb34510ffe498aaed3167575f8992f4716317e63
  commands:
    export:
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
      - default: 0
        help: Max conversations to export; 0 means all loaded history
        name: limit
        required: false
        type: int
      - default: 80
        help: Max history-list scroll rounds when limit is 0 (max 500)
        name: maxScrolls
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs:
      - workspace-relative output
      sensitive_output: []
    export-all:
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
      - default: 0
        help: Max conversations to export; 0 means all loaded history
        name: limit
        required: false
        type: int
      - default: 0
        help: Skip this many conversations before exporting
        name: offset
        required: false
        type: int
      - default: ''
        help: Optional grok/export JSON manifest path; skips history dialog and visits listed /c pages directly
        name: manifestPath
        required: false
        type: string
      - default: 80
        help: Max history-list scroll rounds when limit is 0 (max 500)
        name: maxScrolls
        required: false
        type: int
      - default: 30
        help: Max per-conversation scroll-to-bottom rounds (max 200)
        name: pageScrolls
        required: false
        type: int
      - default: 30000
        help: Max wait for each conversation page to show messages
        name: pageTimeoutMs
        required: false
        type: int
      - default: 0
        help: Minimum polite delay after a conversation page loads
        name: delayMinMs
        required: false
        type: int
      - default: 5000
        help: Maximum polite delay after a conversation page loads
        name: delayMaxMs
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs:
      - workspace-relative output
      sensitive_output: []
---

# Grok: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `export` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Export all visible Grok conversation history metadata | `limit` (int, optional, default=0); `maxScrolls` (int, optional, default=80) |
| `export-all` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Export Grok conversation history and each conversation transcript | `limit` (int, optional, default=0); `offset` (int, optional, default=0); `manifestPath` (string, optional, default=''); `maxScrolls` (int, optional, default=80); `pageScrolls` (int, optional, default=30); `pageTimeoutMs` (int, optional, default=30000); `delayMinMs` (int, optional, default=0); `delayMaxMs` (int, optional, default=5000) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
