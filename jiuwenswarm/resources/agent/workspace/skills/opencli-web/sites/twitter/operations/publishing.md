---
opencli_contract:
  version: 2
  site: twitter
  operation: publishing
  policy_sha256: d3dfdd9f50e334a4672153f072546b8d93fc2b4c68dc2786edab05aea347b96c
  commands:
    list-create:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: List name (max 25 chars)
        name: name
        positional: true
        required: true
        type: string
      - default: ''
        help: Optional list description (max 100 chars)
        name: description
        required: false
        type: string
      - default: public
        help: public | private
        name: mode
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
    post:
      executor: none
      execution_state: disabled
      semantic_effect: public_write
      risk: high
      auth: required
      transport: browser_dom
      strategy: ui
      browser: true
      opencli_version: 1.8.6
      access: write
      args:
      - help: The text content of the tweet
        name: text
        positional: true
        required: true
        type: string
      - help: Image paths, comma-separated, max 4 (jpg/png/gif/webp)
        name: images
        required: false
        type: string
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs:
      - workspace-relative input when declared by adapter
      file_outputs: []
      sensitive_output: []
---

# Twitter: publishing

Publish, create, edit, or upload remote content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `list-create` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Create a new Twitter/X list (returns the new list id) | `name` (string, required, positional); `description` (string, optional, default=''); `mode` (string, optional, default='public') |
| `post` | `disabled` | `public_write` / `high` | Not executable; use the declared fallback if permitted<br>Post a new tweet/thread | `text` (string, required, positional); `images` (string, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
