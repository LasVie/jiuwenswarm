---
opencli_contract:
  version: 2
  site: flomo
  operation: memos
  policy_sha256: c4da9edbd4f5cc5999174676fd5aea2c5d4442f1ecd519452eae512ac7b1da89
  commands:
    memos:
      executor: none
      execution_state: quarantined
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
        help: Number of memos to fetch (1-200)
        name: limit
        required: false
        type: int
        constraints:
          minimum: 1
          maximum: 200
      - help: Only memos updated after this Unix timestamp in seconds
        name: since
        required: false
        type: int
        constraints:
          minimum: 0
      - help: Pagination cursor from a previous memo page
        name: slug
        required: false
        type: str
        constraints:
          pattern: ^[A-Za-z0-9_-]{1,256}$
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

# Flomo: memos

Read private memo content.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `memos` | `quarantined` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List your Flomo memos | `limit` (int, optional, default=20, minimum=1,maximum=200); `since` (int, optional, minimum=0); `slug` (str, optional, pattern=^[A-Za-z0-9_-]{1,256}$) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
