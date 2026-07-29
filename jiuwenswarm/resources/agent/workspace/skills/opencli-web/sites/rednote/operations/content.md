---
opencli_contract:
  version: 2
  site: rednote
  operation: content
  policy_sha256: 211ce3a7c0c5af88335a9c29eb7560a50553d65018de56f5c3e094060c017ea2
  commands:
    comments:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
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
      - default: 20
        help: Number of top-level comments (max 50)
        name: limit
        required: false
        type: int
      - default: false
        help: Include nested replies (楼中楼)
        name: with-replies
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    note:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
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
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    user:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: User id or profile URL
        name: id
        positional: true
        required: true
        type: str
      - default: 15
        help: Number of notes to return
        name: limit
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

# Rednote: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `comments` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read comments from a rednote note (supports nested replies) | `note-id` (str, required, positional); `limit` (int, optional, default=20); `with-replies` (boolean, optional, default=False) |
| `note` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Read note body and engagement counts from a rednote note | `note-id` (str, required, positional) |
| `user` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Get public notes from a rednote user profile | `id` (str, required, positional); `limit` (int, optional, default=15) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
