---
opencli_contract:
  version: 2
  site: zlibrary
  operation: private-content
  policy_sha256: 85f5c89c4696b9a731022a6b7eb28f74f3c3a6f60de4c7c37be095b2cb979140
  commands:
    info:
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
      - help: Z-Library book page URL (e.g. https://z-library.im/book/...)
        name: url
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: none
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    search:
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
      - help: Search keyword (title, author, ISBN, etc.)
        name: query
        positional: true
        required: true
        type: str
      - default: 10
        help: Max results (1–25)
        name: limit
        required: false
        type: int
      confirmation: unsupported
      fallback:
        before_dispatch: none
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
---

# Zlibrary: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `info` | `quarantined` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get book details and available download formats from a Z-Library book page | `url` (str, required, positional) |
| `search` | `quarantined` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Search Z-Library for books by title, author, ISBN, or keyword | `query` (str, required, positional); `limit` (int, optional, default=10) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
