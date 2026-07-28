---
opencli_contract:
  version: 2
  site: xiaoyuzhou
  operation: file-operations
  policy_sha256: 567210bd1cc385a31a214f648eb1031d2bebfc3dbb97188fd7b51f02ca930fc9
  commands:
    download:
      executor: none
      execution_state: disabled
      semantic_effect: local_write
      risk: high
      auth: required
      transport: local
      strategy: local
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Episode ID (eid from podcast-episodes output)
        name: id
        positional: true
        required: true
        type: str
      - default: ./xiaoyuzhou-downloads
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
    transcript:
      executor: none
      execution_state: disabled
      semantic_effect: local_write
      risk: high
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Episode ID (eid from podcast-episodes output)
        name: id
        positional: true
        required: true
        type: str
      - default: ./xiaoyuzhou-transcripts
        help: Output directory
        name: output
        required: false
        type: str
      - default: true
        help: Save transcript JSON file
        name: json
        required: false
        type: boolean
      - default: true
        help: Save extracted transcript text file
        name: text
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs:
      - workspace-relative output
      sensitive_output: []
---

# Xiaoyuzhou: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Download Xiaoyuzhou episode audio | `id` (str, required, positional); `output` (str, optional, default='./xiaoyuzhou-downloads') |
| `transcript` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Download Xiaoyuzhou transcript as JSON and text (requires local credentials) | `id` (str, required, positional); `output` (str, optional, default='./xiaoyuzhou-transcripts'); `json` (boolean, optional, default=True); `text` (boolean, optional, default=True) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
