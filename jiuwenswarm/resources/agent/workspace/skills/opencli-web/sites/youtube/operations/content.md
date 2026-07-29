---
opencli_contract:
  version: 2
  site: youtube
  operation: content
  policy_sha256: 3d5906cc99870a2ef1d70a87acc167b81f0397a620e41320bd3ec7bc994d1617
  commands:
    channel:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Channel ID (UCxxxx) or handle (@name)
        name: id
        positional: true
        required: true
        type: str
      - default: 10
        help: Max recent videos (max 30)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    comments:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: YouTube video URL or video ID
        name: url
        positional: true
        required: true
        type: str
      - default: 20
        help: Max comments (max 100)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    transcript:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: YouTube video URL or video ID
        name: url
        positional: true
        required: true
        type: str
      - help: Language code (e.g. en, zh-Hans). Omit to auto-select
        name: lang
        required: false
        type: str
      - default: grouped
        help: 'Output mode: grouped (readable paragraphs) or raw (every segment)'
        name: mode
        required: false
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs:
      - workspace-relative output
      sensitive_output: []
    video:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: optional
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: YouTube video URL or video ID
        name: url
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Youtube: content

Read one public item, record, page, or resource.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `channel` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get YouTube channel info and recent videos | `id` (str, required, positional); `limit` (int, optional, default=10) |
| `comments` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get YouTube video comments | `url` (str, required, positional); `limit` (int, optional, default=20) |
| `transcript` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get YouTube video transcript/subtitles | `url` (str, required, positional); `lang` (str, optional); `mode` (str, optional, default='grouped') |
| `video` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get YouTube video metadata (title, views, description, etc.) | `url` (str, required, positional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
