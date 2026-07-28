---
opencli_contract:
  version: 2
  site: weread-official
  operation: content
  policy_sha256: 30b07dfc9f4d9329ce4ee190e87ecf7b2f149b7cbc99d034b073df3568170aae
  commands:
    review:
      executor: none
      execution_state: disabled
      semantic_effect: public_read
      risk: low
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
      confirmation: unsupported
      fallback:
        before_dispatch: browser_agent
        after_failure: none
      file_inputs: []
      file_outputs: []
      sensitive_output: []
---

# Weread Official: content

Read site content and metadata.

This is the terminal contract. The same main Agent must read this exact path with SkillTool immediately before invoking `opencli_execute`. Do not delegate the read or execution.

| Command | State | Effect / risk | Exact structured use | Exact arguments |
|---|---|---|---|---|
| `review` | `disabled` | `public_read` / `low` | Not executable; use the declared fallback if permitted<br>Browse public reviews of a WeRead book | `bookId` (str, required, positional); `type` (str, optional, default='all', choices=all,recommend,thumbs-down,newest,neutral); `count` (int, optional, default=20); `max-idx` (int, optional, default=0); `synckey` (int, optional) |

## Safety and fallback

- Unknown commands and arguments are rejected before subprocess start.
- Arguments are rendered from the frozen catalog schema; no shell, arbitrary argv prefix, executable override, or environment override is accepted.
- A `disabled` or `quarantined` command has documentation but no OpenCLI execution authority. Use only its declared browser fallback.
