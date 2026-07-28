---
opencli_contract:
  version: 2
  site: quark
  operation: write-actions
  policy_sha256: e6980b834de239fe5f4a371cc43a78828fb82b03d2e539d74fc5b391dfd79bf9
  commands:
    mkdir:
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
      - help: Folder name
        name: name
        positional: true
        required: true
        type: str
      - help: Parent folder path (resolved by name)
        name: parent
        required: false
        type: str
      - help: Parent folder fid (use directly)
        name: parent-fid
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    mv:
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
      - help: File IDs to move (comma-separated)
        name: fids
        positional: true
        required: true
        type: str
      - default: ''
        help: Destination folder path (required unless --to-fid is set)
        name: to
        required: false
        type: str
      - default: ''
        help: Destination folder ID (overrides --to)
        name: to-fid
        required: false
        type: str
      - default: 120
        help: 'Max seconds for the overall command (default: 120)'
        name: timeout
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    rename:
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
      - help: File ID to rename
        name: fid
        positional: true
        required: true
        type: str
      - help: New file name
        name: name
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    rm:
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
      - help: File IDs to delete (comma-separated)
        name: fids
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
---

# Quark: write-actions

Change remote service state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `mkdir` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a folder in your Quark Drive | `name` (str, required, positional); `parent` (str, optional); `parent-fid` (str, optional) |
| `mv` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Move files to a folder in your Quark Drive | `fids` (str, required, positional); `to` (str, optional, default=''); `to-fid` (str, optional, default=''); `timeout` (int, optional, default=120) |
| `rename` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Rename a file in your Quark Drive | `fid` (str, required, positional); `name` (str, required) |
| `rm` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Delete files from your Quark Drive | `fids` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
