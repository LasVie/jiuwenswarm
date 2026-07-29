---
opencli_contract:
  version: 2
  site: suno
  operation: generation
  policy_sha256: 9631ed82a00218589f6d15384e5a951afdb07e4c6f80bcebaf7ce35e8001d0f0
  commands:
    generate:
      executor: none
      execution_state: disabled
      semantic_effect: quota_consumption
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: Simple-mode description (ignored when --lyrics is provided)
        name: prompt
        positional: true
        required: false
        type: str
      - help: Custom-mode lyrics (with [Verse]/[Chorus] metatags). Triggers Custom mode.
        name: lyrics
        required: false
        type: str
      - help: Custom-mode style tags (genre, BPM, instruments...). Used with --lyrics.
        name: tags
        required: false
        type: str
      - help: Custom-mode style exclusions (e.g. "no vocals, no autotune"). Used with --lyrics.
        name: negative-tags
        required: false
        type: str
      - help: 'Song title (default: auto-derived from prompt)'
        name: title
        required: false
        type: str
      - default: false
        help: No vocals
        name: instrumental
        required: false
        type: boolean
      - help: 'Model id: chirp-fenix, chirp-bluejay, chirp-v4, chirp-v3-5. Default: chirp-fenix'
        name: model
        required: false
        type: str
      - help: 'Creative weirdness slider (0..1). Default: 0.5'
        name: weirdness
        required: false
        type: str
      - help: 'Style adherence slider (0..1). Default: 0.5'
        name: style-weight
        required: false
        type: str
      - help: 'Comma-separated download formats: mp3, m4a, wav, video, cover, metadata. Default: mp3,metadata'
        name: formats
        required: false
        type: str
      - help: 'Output directory (default: ~/Music/suno)'
        name: op
        required: false
        type: str
      - default: 300
        help: 'Max seconds to wait for clips to finish (default: 300)'
        name: timeout
        required: false
        type: int
      - default: false
        help: Skip download; only print clip ids and Suno URLs
        name: sd
        required: false
        type: boolean
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
      file_outputs: []
      sensitive_output: []
---

# Suno: generation

Generate remote content, start AI work, or consume quota.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `generate` | `disabled` | `quota_consumption` / `high` | Not executable; use the declared fallback if permitted<br>Generate music with Suno (V5.5 chirp-fenix by default) and download clips locally | `prompt` (str, optional, positional); `lyrics` (str, optional); `tags` (str, optional); `negative-tags` (str, optional); `title` (str, optional); `instrumental` (boolean, optional, default=False); `model` (str, optional); `weirdness` (str, optional); `style-weight` (str, optional); `formats` (str, optional); `op` (str, optional); `timeout` (int, optional, default=300); `sd` (boolean, optional, default=False); `confirm-paid` (boolean, optional, default=False) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
