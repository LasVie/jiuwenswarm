---
opencli_contract:
  version: 2
  site: weread-official
  operation: content
  policy_sha256: d16f3266d955da66267fd7e1dbaf9cdfc6ea30567dde1ce258059361ff600b3d
  commands:
    book:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    notes:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    readdata:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    review:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
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
      - choices:
        - all
        - recommend
        - thumbs-down
        - newest
        - neutral
        default: all
        help: Review filter (all/recommend/thumbs-down/newest/neutral)
        name: type
        required: false
        type: str
      - default: 20
        help: Page size (1-100, default 20)
        name: count
        required: false
        type: int
      - default: 0
        help: Pagination cursor — pass idx from last row of previous page
        name: max-idx
        required: false
        type: int
      - help: Sync cursor returned by previous response
        name: synckey
        required: false
        type: int
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
    shelf:
      executor: generic_manifest_read
      execution_state: enabled
      semantic_effect: public_read
      risk: low
      auth: none
      transport: public_http
      strategy: public
      browser: false
      opencli_version: 1.8.6
      access: read
      args: []
      confirmation: none
      fallback:
        before_dispatch: browser_agent
        after_failure: browser_agent
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Weread Official: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `book` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread-official", operation="content", command="book", arguments={"bookId":"<bookId>"})`<br>Show WeRead book metadata, chapters, and reading progress | `bookId` (str, required, positional); `no-chapters` (boolean, optional, default=False); `no-progress` (boolean, optional, default=False) |
| `notes` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread-official", operation="content", command="notes")`<br>List notebooks overview or merged highlights+thoughts for a book | `bookId` (str, optional, positional); `count` (int, optional, default=20); `last-sort` (int, optional) |
| `readdata` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread-official", operation="content", command="readdata")`<br>Reading statistics: time, streak, preferences, top books | `mode` (str, optional, default='monthly', choices=weekly,monthly,annually,overall); `base-time` (int, optional) |
| `review` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread-official", operation="content", command="review", arguments={"bookId":"<bookId>"})`<br>Browse public reviews of a WeRead book | `bookId` (str, required, positional); `type` (str, optional, default='all', choices=all,recommend,thumbs-down,newest,neutral); `count` (int, optional, default=20); `max-idx` (int, optional, default=0); `synckey` (int, optional) |
| `shelf` | `enabled` | `public_read` / `low` | `opencli_execute(site="weread-official", operation="content", command="shelf")`<br>Sync your WeRead shelf (books + albums + article bookmark entry) via the official gateway | none |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- These commands are reviewed public reads. A proven pre-dispatch failure and a read failure may use `browser_agent` once; never run both paths concurrently.
