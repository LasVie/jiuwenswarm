---
opencli_contract:
  version: 2
  site: tieba
  operation: content
  policy_sha256: 239c0f008bb350c840d9f8f253b634481a32f077945d1bd31e7d601e734cc952
  commands:
    read:
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
      - help: Thread ID
        name: id
        positional: true
        required: true
        type: string
      - default: 1
        help: Page number
        name: page
        required: false
        type: int
      - default: 30
        help: Number of replies to return
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

# Tieba: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `read` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read a tieba thread | `id` (string, required, positional); `page` (int, optional, default=1); `limit` (int, optional, default=30) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
