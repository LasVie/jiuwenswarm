---
opencli_contract:
  version: 2
  site: brave
  operation: private-content
  policy_sha256: 3076997816d4c7a5ec356c0adf4749e15cc6f9abd8ab3d0aac67f6ddfa064065
  commands:
    search:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: browser_dom
      strategy: public
      browser: true
      opencli_version: 1.8.6
      access: read
      args:
      - help: Search query
        name: keyword
        positional: true
        required: true
        type: str
      - default: 10
        help: Number of results per page (max 18)
        name: limit
        required: false
        type: int
      - default: 0
        help: Page offset (0, 1, 2...). Brave returns ~18 results per page
        name: offset
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

# Brave: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `search` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search Brave Search | `keyword` (str, required, positional); `limit` (int, optional, default=10); `offset` (int, optional, default=0) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
