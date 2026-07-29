---
opencli_contract:
  version: 2
  site: tiktok
  operation: content
  policy_sha256: 3442947251dff64808dcca780e0776b04a96d6a79525a6606459b850e8bbc53f
  commands:
    profile:
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
      - help: TikTok username (without @)
        name: username
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
    user:
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
      - help: TikTok username (without @)
        name: username
        positional: true
        required: true
        type: str
      - default: 20
        help: Number of videos to return (max 120)
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
---

# Tiktok: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `profile` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get TikTok user profile info | `username` (str, required, positional) |
| `user` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get recent videos from a TikTok user via page-context APIs | `username` (str, required, positional); `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
