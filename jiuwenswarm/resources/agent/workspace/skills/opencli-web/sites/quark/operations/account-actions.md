---
opencli_contract:
  version: 2
  site: quark
  operation: account-actions
  policy_sha256: 07f7880a2065b6b2d8bfbfe88c814ecbfdf48097b97888035ceda06ae77d83b0
  commands:
    save:
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
      - help: Quark share URL or pwd_id
        name: url
        positional: true
        required: true
        type: str
      - default: ''
        help: Destination folder path
        name: to
        required: false
        type: str
      - default: ''
        help: Destination folder ID (overrides --to)
        name: to-fid
        required: false
        type: str
      - default: ''
        help: File IDs to save (comma-separated, from share-tree). Omit to save all.
        name: fids
        required: false
        type: str
      - default: ''
        help: Share token (from share-tree output, required with --fids)
        name: stoken
        required: false
        type: str
      - default: ''
        help: Share passcode (if required)
        name: passcode
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
---

# Quark: account-actions

Change reversible account relationship or saved state.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `save` | `disabled` | `reversible_remote_write` / `high` | Not executable; use the declared fallback if permitted<br>Save shared files to your Quark Drive | `url` (str, required, positional); `to` (str, optional, default=''); `to-fid` (str, optional, default=''); `fids` (str, optional, default=''); `stoken` (str, optional, default=''); `passcode` (str, optional, default=''); `timeout` (int, optional, default=120) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
