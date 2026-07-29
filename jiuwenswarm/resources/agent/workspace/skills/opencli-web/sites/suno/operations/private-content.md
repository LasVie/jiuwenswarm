---
opencli_contract:
  version: 2
  site: suno
  operation: private-content
  policy_sha256: 9631ed82a00218589f6d15384e5a951afdb07e4c6f80bcebaf7ce35e8001d0f0
  commands:
    list:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_cookie
      strategy: cookie
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - default: 20
        help: 'Max clips to list (default: 20)'
        name: limit
        required: false
        type: int
      - default: 0
        help: 'Pagination offset, 0-based (default: 0)'
        name: page
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Suno: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `list` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List recent Suno clips in your library (id, title, status, created_at, link) | `limit` (int, optional, default=20); `page` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
