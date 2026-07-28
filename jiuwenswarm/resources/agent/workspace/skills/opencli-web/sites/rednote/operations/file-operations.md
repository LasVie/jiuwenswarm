---
opencli_contract:
  version: 2
  site: rednote
  operation: file-operations
  policy_sha256: e74eb27b8de6e5cfbe7c9e82937ac7994460405b9d6ab27989389a959792e5bc
  commands:
    download:
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
      - help: Full rednote note URL with xsec_token
        name: note-id
        positional: true
        required: true
        type: str
      - default: ./rednote-downloads
        help: Output directory
        name: output
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

# Rednote: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Download images and videos from a rednote note | `note-id` (str, required, positional); `output` (str, optional, default='./rednote-downloads') |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
