---
opencli_contract:
  version: 2
  site: weread-official
  operation: private-content
  policy_sha256: 30b07dfc9f4d9329ce4ee190e87ecf7b2f149b7cbc99d034b073df3568170aae
  commands:
    book:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: WeRead bookId (from `weread-official search`)
        name: bookId
        positional: true
        required: true
        type: str
      - default: false
        help: Skip /book/chapterinfo call
        name: no-chapters
        required: false
        type: boolean
      - default: false
        help: Skip /book/getprogress call
        name: no-progress
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
    discover:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Anchor bookId for similar-book mode; omit for personalized recommendations
        name: bookId
        positional: true
        required: false
        type: str
      - default: 12
        help: Page size (default 12)
        name: count
        required: false
        type: int
      - default: 0
        help: 'Pagination cursor (recommend: previous searchIdx; similar: previous idx)'
        name: max-idx
        required: false
        type: int
      - help: Carry-forward sessionId for /book/similar paging
        name: session-id
        required: false
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
    notes:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - help: Limit to one book; omit for full notebook overview
        name: bookId
        positional: true
        required: false
        type: str
      - default: 20
        help: Page size for the notebooks overview (1-100)
        name: count
        required: false
        type: int
      - help: 'Cursor: pass previous page sort value to fetch the next page (/user/notebooks)'
        name: last-sort
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
    readdata:
      executor: none
      execution_state: disabled
      semantic_effect: private_content_read
      risk: medium
      auth: required
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args:
      - choices:
        - weekly
        - monthly
        - annually
        - overall
        default: monthly
        help: 'Stat window: weekly / monthly / annually / overall'
        name: mode
        required: false
        type: str
      - help: Optional Unix timestamp inside the target period; default is current period
        name: base-time
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
      transport: public_http
      strategy: public
      browser: false
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
---

# Weread Official: private-content

Read credential-gated personal WeRead content and account activity.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `book` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Show WeRead book metadata, chapters, and reading progress | `bookId` (str, required, positional); `no-chapters` (boolean, optional, default=False); `no-progress` (boolean, optional, default=False) |
| `discover` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Personalized or similar-book recommendations from WeRead | `bookId` (str, optional, positional); `count` (int, optional, default=12); `max-idx` (int, optional, default=0); `session-id` (str, optional) |
| `notes` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>List notebooks overview or merged highlights+thoughts for a book | `bookId` (str, optional, positional); `count` (int, optional, default=20); `last-sort` (int, optional) |
| `readdata` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Reading statistics: time, streak, preferences, top books | `mode` (str, optional, default='monthly', choices=weekly,monthly,annually,overall); `base-time` (int, optional) |
| `shelf` | `disabled` | `private_content_read` / `medium` | Not executable; use the declared fallback if permitted<br>Sync your WeRead shelf (books + albums + article bookmark entry) via the official gateway | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
- Any operation that may change state, expose private data, write a file, or consume quota is fail-closed after dispatch and cannot be automatically retried through a browser.
