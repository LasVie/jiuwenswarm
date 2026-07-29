---
opencli_contract:
  version: 2
  site: suno
  operation: file-operations
  policy_sha256: 9631ed82a00218589f6d15384e5a951afdb07e4c6f80bcebaf7ce35e8001d0f0
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
      access: write
      args:
      - help: Clip UUID or https://suno.com/song/<id> URL
        name: clip
        positional: true
        required: true
        type: str
      - help: 'Comma-separated formats: mp3, m4a, wav, video, cover, metadata. Default: mp3,metadata'
        name: formats
        required: false
        type: str
      - help: 'Output directory (default: ~/Music/suno)'
        name: op
        required: false
        type: str
      - default: false
        help: Required to allow paid downloads (wav). Without it, paid formats are skipped with a warning.
        name: confirm-paid
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

# Suno: file-operations

Create or download workspace files.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `download` | `disabled` | `local_write` / `high` | Not executable; use the declared fallback if permitted<br>Download an existing Suno clip (MP3 + optional WAV/M4A/video) by id | `clip` (str, required, positional); `formats` (str, optional); `op` (str, optional); `confirm-paid` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
