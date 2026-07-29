---
opencli_contract:
  version: 2
  site: quark
  operation: private-content
  policy_sha256: 07f7880a2065b6b2d8bfbfe88c814ecbfdf48097b97888035ceda06ae77d83b0
  commands:
    ls:
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
      - default: ''
        help: Folder path to list (empty for root)
        name: path
        positional: true
        required: false
        type: str
      - default: 0
        help: Max depth to traverse
        name: depth
        required: false
        type: int
      - default: false
        help: Show directories only
        name: dirs-only
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    share-tree:
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
      - help: Quark share URL or pwd_id
        name: url
        positional: true
        required: true
        type: str
      - default: ''
        help: Share passcode (if required)
        name: passcode
        required: false
        type: str
      - default: 10
        help: Max directory depth
        name: depth
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

# Quark: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ls` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List files in your Quark Drive | `path` (str, optional, positional, default=''); `depth` (int, optional, default=0); `dirs-only` (boolean, optional, default=False) |
| `share-tree` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get directory tree from Quark Drive share link as nested JSON | `url` (str, required, positional); `passcode` (str, optional, default=''); `depth` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
