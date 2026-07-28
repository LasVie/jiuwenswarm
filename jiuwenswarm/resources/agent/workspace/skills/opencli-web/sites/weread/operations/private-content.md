---
opencli_contract:
  version: 2
  site: weread
  operation: private-content
  policy_sha256: fe850910e20949248d867b786fb8ba6f525ea8a61d6b349ac040bef7c4f02ebb
  commands:
    ai-outline:
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
      - help: Book ID (from shelf or search results)
        name: book-id
        positional: true
        required: true
        type: str
      - default: 200
        help: Max outline items to return
        name: limit
        required: false
        type: int
      - default: 4
        help: Max outline depth (2=topics, 3=key points, 4=details)
        name: depth
        required: false
        type: int
      - default: false
        help: Output structured rows (chapter/idx/level/text) for programmatic use
        name: raw
        required: false
        type: boolean
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    book:
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
      - help: Book ID from search or shelf results
        name: book-id
        positional: true
        required: true
        type: str
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    highlights:
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
      - help: Book ID (from shelf or search results)
        name: book-id
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results
        name: limit
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
    notebooks:
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
      args: []
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output:
      - private content
      - account identifiers
    notes:
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
      - help: Book ID (from shelf or search results)
        name: book-id
        positional: true
        required: true
        type: str
      - default: 20
        help: Max results
        name: limit
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
    shelf:
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
        help: Max results
        name: limit
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

# Weread: private-content

Read content that depends on an authenticated account.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `ai-outline` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Get AI-generated outline for a book | `book-id` (str, required, positional); `limit` (int, optional, default=200); `depth` (int, optional, default=4); `raw` (boolean, optional, default=False) |
| `book` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>View book details on WeRead | `book-id` (str, required, positional) |
| `highlights` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List your highlights (underlines) in a book | `book-id` (str, required, positional); `limit` (int, optional, default=20) |
| `notebooks` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List books that have highlights or notes | none |
| `notes` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List your notes (thoughts) on a book | `book-id` (str, required, positional); `limit` (int, optional, default=20) |
| `shelf` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List books on your WeRead bookshelf | `limit` (int, optional, default=20) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
